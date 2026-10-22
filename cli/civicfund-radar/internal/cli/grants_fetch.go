package cli

import (
	"github.com/spf13/cobra"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
)

func newGrantsfetchCmd() *cobra.Command {
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "fetch <opportunity-id>",
		Short: "Fetch a Grants.gov opportunity detail record",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			record, err := civicfundradar.GrantsFetch(cmd.Context(), args[0])
			if err != nil {
				return err
			}
			if asJSON {
				return printJSON(cmd.OutOrStdout(), record)
			}
			return printJSON(cmd.OutOrStdout(), record)
		},
	}
	addJSONFlag(cmd, &asJSON)
	return cmd
}
