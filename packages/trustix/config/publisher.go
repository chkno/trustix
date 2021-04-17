// Copyright (C) 2021 Tweag IO
//
// This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
//
// This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

package config

import (
	signer "github.com/tweag/trustix/packages/trustix/config/signer"
)

type Publisher struct {
	Signer    *signer.Signer    `toml:"signer"`
	PublicKey *PublicKey        `toml:"key"`
	Meta      map[string]string `toml:"meta"`
}

func (p *Publisher) Validate() error {
	if err := p.Signer.Validate(); err != nil {
		return err
	}

	return nil
}
