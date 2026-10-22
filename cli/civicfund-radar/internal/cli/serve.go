// Copyright 2026 OpenProse contributors. Licensed under MIT. See LICENSE.

package cli

import (
	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
	"github.com/spf13/cobra"
)

func newServeCmd() *cobra.Command {
	var port int
	var dbPath string
	cmd := &cobra.Command{
		Use:   "serve",
		Short: "Start the CivicFund Radar local web application and API server",
		RunE: func(cmd *cobra.Command, args []string) error {
			return civicfundradar.StartWebServer(cmd.Context(), port, dbPath)
		},
	}
	cmd.Flags().IntVarP(&port, "port", "p", 8080, "Port to listen on")
	addDBFlag(cmd, &dbPath)
	return cmd
}
