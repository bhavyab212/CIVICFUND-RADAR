package cli

import (
	"github.com/spf13/cobra"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
)

func newGrantssearchCmd() *cobra.Command {
	var keyword string
	var oppNum string
	var rows int
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "search",
		Short: "Search the Grants.gov Applicant API",
		RunE: func(cmd *cobra.Command, args []string) error {
			records, err := civicfundradar.GrantsSearch(cmd.Context(), keyword, rows, oppNum)
			if err != nil {
				return err
			}
			if asJSON {
				return printJSON(cmd.OutOrStdout(), records)
			}
			table := [][]string{{"NUMBER", "TITLE", "SPONSOR", "DEADLINE", "URL"}}
			for _, r := range records {
				table = append(table, []string{r.FundingOpportunityNumber, truncate(r.Title, 70), r.Agency, r.CloseDate, r.URL})
			}
			printRows(cmd.OutOrStdout(), table)
			return nil
		},
	}
	cmd.Flags().StringVar(&keyword, "keyword", "SBIR", "Keyword query")
	cmd.Flags().StringVar(&oppNum, "opp-num", "", "Funding opportunity number")
	cmd.Flags().IntVar(&rows, "rows", 10, "Number of rows")
	addJSONFlag(cmd, &asJSON)
	return cmd
}
