package edu.toronto.cs.cute.utils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import edu.toronto.cs.cute.weight.WeightFunction;

public class Utils {

	static public Map<String, Map<String, Double>> parseTermFrequencyFromFile(
			String path, String separator, Double topTerms,
			WeightFunction weightFunction) throws IOException {
		Map<String, Map<String, Double>> termFrequencyMap =
				new HashMap<String, Map<String,Double>>();
		BufferedReader reader = new BufferedReader(new FileReader(path));
		String line;
		while ((line = reader.readLine()) != null) {
			String[] lineSplitted = line.split(separator);
			String term = lineSplitted[0];
			String frequency = lineSplitted[1];
			String protocol = lineSplitted[2];
			Map<String, Double> protocolMap = termFrequencyMap.get(term);
			if (protocolMap == null) {
				protocolMap = new HashMap<String, Double>();
				termFrequencyMap.put(term, protocolMap);
			}
			protocolMap.put(protocol, new Double(frequency));
		}
		return weightFunction.weight(termFrequencyMap);
	}

}
