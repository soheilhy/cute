// Copyright 2011 HiPerNet Research Group, University of Toronto.. All Rights
// Reserved.
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

package edu.toronto.cs.cute;

import java.util.List;
import java.util.Map;

/**
 * All classification algorithms must implement this interface.
 * 
 * @author Soheil Hassas Yeganeh <soheil@cs.toronto.edu>
 */
public abstract class Classifier {
	
	protected Map<String, Map<String, Double>> weightedTerm;

	/**
	 * @param weightedTerms The map of weighted terms for protocols
	 * 		(protocols->term->weight).
	 */
	public Classifier(Map<String, Map<String, Double>> weightedTerms) {
		this.weightedTerm = weightedTerms;
	}
	
	/**
	 * Classifies the given payload. 
	 *
	 * @param payload The application layer payload.
	 * @return The list of protocols for the payload.
	 */
	public abstract List<String> classify(String payload);
}
