package edu.toronto.cs.cute.weight;

import java.util.Map;

/**
 * Traffic classification weight function.
 *
 * @author Soheil Hassas Yeganeh <soheil@cs.toronto.edu>
 *
 */
public interface WeightFunction {

	/**
	 * Weight a set of terms according to their frequency.
	 * @param termFrequencyMap A frequency term map (term->protocol->frequency). 
	 * @return A weighted term map (protocol->term->frequency).
	 */
	Map<String, Map<String, Double>> weight(
			Map<String, Map<String, Double>> termFrequencyMap);

}
