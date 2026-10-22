// Copyright 2026 OpenProse contributors. Licensed under MIT. See LICENSE.

package main

import (
	"fmt"
	"os"

	"github.com/bhavyab212/civicfund-radar/cli/civicfund-radar/internal/cli"
)

func main() {
	if err := cli.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		os.Exit(cli.ExitCode(err))
	}
}
