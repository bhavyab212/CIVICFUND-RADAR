package cli

import (
	"fmt"
	"io"
	"os"

	"github.com/spf13/cobra"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/civicfundradar"
)

func newResearchCmd() *cobra.Command {
	var dbPath string
	var assignmentPath string
	var limit int
	var refresh string
	var semantic string
	var asJSON bool
	var compact bool
	var selectFields string
	var includeInactive bool
	cmd := &cobra.Command{
		Use:   "research",
		Short: "Return an agent-ready grant research packet",
		Long:  "Return an agent-ready grant research packet from a resolved startup assignment. The command is deterministic and does not call an LLM.",
		RunE: func(cmd *cobra.Command, args []string) error {
			assignment, err := readAssignment(assignmentPath)
			if err != nil {
				return err
			}
			packet, err := civicfundradar.Research(cmd.Context(), civicfundradar.ResearchOptions{
				DBPath:          dbPath,
				Limit:           limit,
				Refresh:         refresh,
				Semantic:        semantic,
				Compact:         compact,
				IncludeInactive: includeInactive,
			}, assignment)
			if err != nil {
				return err
			}
			if asJSON || compact || selectFields != "" {
				return printJSONWithOptions(cmd.OutOrStdout(), packet, outputOptions{Select: selectFields, Compact: compact})
			}
			rows := [][]string{{"FIT", "PROGRAM", "AGENCY", "DEADLINE", "URL"}}
			for _, grant := range packet.Grants {
				deadline := ""
				if grant.Deadline != nil {
					deadline = *grant.Deadline
				}
				rows = append(rows, []string{grant.EligibilityFit.Level, truncate(grant.ProgramName, 60), truncate(grant.Agency, 28), deadline, grant.URL})
			}
			printRows(cmd.OutOrStdout(), rows)
			return nil
		},
	}
	addDBFlag(cmd, &dbPath)
	addLimitFlag(cmd, &limit, 10)
	addJSONFlag(cmd, &asJSON)
	addSelectFlag(cmd, &selectFields)
	cmd.Flags().StringVar(&assignmentPath, "assignment", "", "Research assignment JSON path, or '-' for stdin")
	cmd.Flags().StringVar(&refresh, "refresh", "auto", "Refresh mode: auto or off")
	cmd.Flags().StringVar(&semantic, "semantic", "auto", "Semantic retrieval mode: auto, usearch, or off")
	cmd.Flags().BoolVar(&includeInactive, "include-inactive", false, "Include closed, archived, or past-due opportunities")
	addCompactFlag(cmd, &compact)
	return cmd
}

func readAssignment(path string) (civicfundradar.Assignment, error) {
	if path == "" {
		return civicfundradar.Assignment{}, fmt.Errorf("--assignment is required; pass a JSON file or '-' for stdin")
	}
	var data []byte
	var err error
	if path == "-" {
		data, err = io.ReadAll(os.Stdin)
	} else {
		data, err = os.ReadFile(path)
	}
	if err != nil {
		return civicfundradar.Assignment{}, err
	}
	return civicfundradar.ParseAssignment(data)
}
