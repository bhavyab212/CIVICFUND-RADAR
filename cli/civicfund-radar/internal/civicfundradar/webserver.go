// Copyright 2026 OpenProse contributors. Licensed under MIT. See LICENSE.

package civicfundradar

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// StartWebServer launches the CivicFund Radar local HTTP API and frontend dashboard.
func StartWebServer(ctx context.Context, port int, dbPath string) error {
	mux := http.NewServeMux()

	// 1. Health check
	mux.HandleFunc("/api/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		feeds, _ := Feeds()
		sources, _ := Sources()
		client := NewTinyFishClient()

		mode := "verified_registry"
		if client.HasLiveKey() {
			mode = "live_tinyfish"
		}

		_ = json.NewEncoder(w).Encode(map[string]any{
			"status":             "healthy",
			"product":            "CivicFund Radar",
			"version":            "1.0.0",
			"mode":               mode,
			"feeds_count":        len(feeds),
			"sources_count":      len(sources),
			"no_llm_invariant":   true,
			"semantic_retrieval": "usearch preferred, FTS5 fallback",
		})
	})

	// 2. Opportunities Search API (POST /api/opportunities/search)
	mux.HandleFunc("/api/opportunities/search", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.Method != http.MethodPost {
			http.Error(w, `{"error":"Method not allowed; use POST"}`, http.StatusMethodNotAllowed)
			return
		}

		var req ProfileRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			// If body empty, default to Harbor Community Climate Alliance
			req = ProfileRequest{
				OrganizationName: "Harbor Community Climate Alliance",
				OrganizationType: "501(c)(3) Non-Profit",
				CountryOrRegion:  "United States",
				ProjectSummary:   "Community microgrids, urban heat island mitigation, and coastal stormwater resilience.",
				FocusAreas:       []string{"Community Microgrids", "Urban Heat Island", "Environmental Justice", "Clean Energy"},
				Justice40:        true,
			}
		}

		store, err := OpenStore(ctx, dbPath)
		if err != nil {
			store = nil
		} else {
			defer store.Close()
		}

		resp, err := DiscoverAndMatch(r.Context(), req, store)
		if err != nil {
			http.Error(w, fmt.Sprintf(`{"error":"%v"}`, err), http.StatusInternalServerError)
			return
		}

		_ = json.NewEncoder(w).Encode(resp)
	})

	// 3. Web UI static handler
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Try to serve from web/ directory if it exists
		cwd, _ := os.Getwd()
		candidates := []string{
			filepath.Join(cwd, "web", "index.html"),
			filepath.Join(cwd, "..", "web", "index.html"),
			filepath.Join(cwd, "..", "..", "web", "index.html"),
		}

		for _, p := range candidates {
			if data, err := os.ReadFile(p); err == nil {
				w.Header().Set("Content-Type", "text/html; charset=utf-8")
				w.Write(data)
				return
			}
		}

		// Fallback minimal HTML
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprintf(w, "<html><body><h1>CivicFund Radar</h1><p>Running on port %d</p></body></html>", port)
	})

	addr := fmt.Sprintf(":%d", port)
	server := &http.Server{
		Addr:              addr,
		Handler:           corsMiddleware(mux),
		ReadHeaderTimeout: 10 * time.Second,
	}

	fmt.Printf("CivicFund Radar Web Dashboard running at http://localhost:%d\n", port)
	fmt.Printf("API Endpoints available:\n  - POST /api/opportunities/search\n  - GET  /api/health\n")

	return server.ListenAndServe()
}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}
