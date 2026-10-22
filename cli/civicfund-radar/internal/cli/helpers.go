package cli

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"strconv"
	"strings"
	"unicode"
	"unicode/utf8"

	"github.com/spf13/cobra"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
)

func printJSON(w io.Writer, v any) error {
	enc := json.NewEncoder(w)
	enc.SetIndent("", "  ")
	return enc.Encode(v)
}

type outputOptions struct {
	Select  string
	Compact bool
}

func printJSONWithOptions(w io.Writer, v any, opts outputOptions) error {
	out := v
	if strings.TrimSpace(opts.Select) != "" {
		out = selectJSONFields(v, opts.Select)
	}
	enc := json.NewEncoder(w)
	if !opts.Compact {
		enc.SetIndent("", "  ")
	}
	return enc.Encode(out)
}

func selectJSONFields(v any, selectExpr string) map[string]any {
	var raw any
	data, err := json.Marshal(v)
	if err != nil {
		return map[string]any{"error": "select failed: " + err.Error()}
	}
	if err := json.Unmarshal(data, &raw); err != nil {
		return map[string]any{"error": "select failed: " + err.Error()}
	}
	out := map[string]any{}
	for _, part := range strings.Split(selectExpr, ",") {
		path := strings.TrimSpace(part)
		if path == "" {
			continue
		}
		out[path] = valuesAtPath(raw, strings.Split(path, "."))
	}
	return out
}

func valuesAtPath(v any, parts []string) any {
	if len(parts) == 0 {
		return v
	}
	switch cur := v.(type) {
	case map[string]any:
		next, ok := cur[parts[0]]
		if !ok {
			return nil
		}
		return valuesAtPath(next, parts[1:])
	case []any:
		values := make([]any, 0, len(cur))
		for _, item := range cur {
			values = append(values, valuesAtPath(item, parts))
		}
		return values
	default:
		return nil
	}
}

func printRows(w io.Writer, rows [][]string) {
	for _, row := range rows {
		fmt.Fprintln(w, strings.Join(row, "\t"))
	}
}

func addDBFlag(cmd *cobra.Command, dbPath *string) {
	cmd.Flags().StringVar(dbPath, "db", civicfundradar.DefaultDBPath(), "SQLite database path")
}

func addJSONFlag(cmd *cobra.Command, asJSON *bool) {
	cmd.Flags().BoolVar(asJSON, "json", false, "Print JSON output")
}

func addSelectFlag(cmd *cobra.Command, selectFields *string) {
	cmd.Flags().StringVar(selectFields, "select", "", "Comma-separated JSON fields to return")
}

func addCompactFlag(cmd *cobra.Command, compact *bool) {
	cmd.Flags().BoolVar(compact, "compact", false, "Print compact JSON")
}

func addLimitFlag(cmd *cobra.Command, limit *int, value int) {
	cmd.Flags().IntVar(limit, "limit", value, "Maximum rows to return")
}

func openStore(ctx context.Context, dbPath string) (*civicfundradar.Store, error) {
	return civicfundradar.OpenStore(ctx, dbPath)
}

func ensureReadOnlySQL(query string) error {
	q := strings.TrimSpace(query)
	token, ok := firstSQLToken(q)
	if !ok {
		return fmt.Errorf("only read-only SQL is allowed (SELECT, WITH, PRAGMA)")
	}
	switch strings.ToLower(token) {
	case "select", "with", "pragma":
	default:
		return fmt.Errorf("only read-only SQL is allowed (SELECT, WITH, PRAGMA)")
	}
	if hasStackedSQLStatement(q) {
		return fmt.Errorf("only one read-only SQL statement is allowed")
	}
	if containsMutatingSQLKeyword(q) {
		return fmt.Errorf("mutating SQL statements are not allowed")
	}
	return nil
}

func containsMutatingSQLKeyword(query string) bool {
	inSingle := false
	inDouble := false
	var token strings.Builder
	checkToken := func() bool {
		t := strings.ToLower(token.String())
		token.Reset()
		switch t {
		case "insert", "update", "delete", "drop", "alter", "create", "replace", "attach", "detach":
			return true
		}
		return false
	}
	for i := 0; i < len(query); i++ {
		ch := query[i]
		switch ch {
		case '\'':
			if inSingle && i+1 < len(query) && query[i+1] == '\'' {
				i++
				continue
			}
			if !inDouble {
				inSingle = !inSingle
			}
			if checkToken() {
				return true
			}
		case '"':
			if inDouble && i+1 < len(query) && query[i+1] == '"' {
				i++
				continue
			}
			if !inSingle {
				inDouble = !inDouble
			}
			if checkToken() {
				return true
			}
		default:
			if !inSingle && !inDouble {
				if (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9') || ch == '_' {
					token.WriteByte(ch)
				} else {
					if checkToken() {
						return true
					}
				}
			}
		}
	}
	return checkToken()
}

func firstSQLToken(query string) (string, bool) {
	query = strings.TrimLeftFunc(query, unicode.IsSpace)
	if query == "" {
		return "", false
	}
	end := 0
	for end < len(query) {
		r, size := utf8.DecodeRuneInString(query[end:])
		if r == utf8.RuneError && size == 1 {
			break
		}
		if !unicode.IsLetter(r) {
			break
		}
		end += size
	}
	if end == 0 {
		return "", false
	}
	return query[:end], true
}

func hasStackedSQLStatement(query string) bool {
	inSingle := false
	inDouble := false
	for i := 0; i < len(query); i++ {
		switch query[i] {
		case '\'':
			if inSingle && i+1 < len(query) && query[i+1] == '\'' {
				i++
				continue
			}
			if !inDouble {
				inSingle = !inSingle
			}
		case '"':
			if inDouble && i+1 < len(query) && query[i+1] == '"' {
				i++
				continue
			}
			if !inSingle {
				inDouble = !inDouble
			}
		case ';':
			if !inSingle && !inDouble && strings.TrimSpace(query[i+1:]) != "" {
				return true
			}
		}
	}
	return false
}

func queryRows(ctx context.Context, db *sql.DB, query string, args ...any) ([]map[string]any, error) {
	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	cols, err := rows.Columns()
	if err != nil {
		return nil, err
	}
	var out []map[string]any
	for rows.Next() {
		values := make([]any, len(cols))
		ptrs := make([]any, len(cols))
		for i := range values {
			ptrs[i] = &values[i]
		}
		if err := rows.Scan(ptrs...); err != nil {
			return nil, err
		}
		record := map[string]any{}
		for i, col := range cols {
			switch v := values[i].(type) {
			case []byte:
				record[col] = string(v)
			default:
				record[col] = v
			}
		}
		out = append(out, record)
	}
	return out, rows.Err()
}

func fmtInt(v int) string {
	return strconv.Itoa(v)
}

func fmtAny(v any) string {
	return fmt.Sprint(v)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	if n <= 3 {
		return s[:n]
	}
	return s[:n-3] + "..."
}
