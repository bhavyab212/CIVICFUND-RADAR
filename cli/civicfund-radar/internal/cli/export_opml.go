package cli

import (
	"os"

	"github.com/spf13/cobra"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
)

func newExportopmlCmd() *cobra.Command {
	var output string
	cmd := &cobra.Command{
		Use:   "opml",
		Short: "Write the grouped civicfund-radar OPML feed list",
		RunE: func(cmd *cobra.Command, args []string) error {
			data := civicfundradar.OPML()
			if output == "" || output == "-" {
				_, err := cmd.OutOrStdout().Write(data)
				return err
			}
			return os.WriteFile(output, data, 0o644)
		},
	}
	cmd.Flags().StringVarP(&output, "output", "o", "-", "Output path, or - for stdout")
	return cmd
}
