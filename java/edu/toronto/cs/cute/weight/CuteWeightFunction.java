package edu.toronto.cs.cute.weight;

import java.util.HashMap;
import java.util.Map;

public class CuteWeightFunction implements WeightFunction {

	private double rho;
	private double frequencyThreshold;

	public CuteWeightFunction(double rho, double frequencyThreshold) {
		this.rho = rho;
		this.frequencyThreshold = frequencyThreshold;
  }

	/**
	 * {@inheritDoc}
	 */
	@Override
  public Map<String, Map<String, Double>> weight(
      Map<String, Map<String, Double>> termFrequencyMap) {
    Map<String, Map<String, Double>> protocolMap =
    		new HashMap<String, Map<String,Double>>();
    for (Map.Entry<String, Map<String, Double>> entry :
    		termFrequencyMap.entrySet()) {
    	double sumOfFrequencies = 0;
    	for (Double freq : entry.getValue().values()) {
    		sumOfFrequencies += freq;
    	}
    	
    	String term = entry.getKey();

    	for (Map.Entry<String, Double> protocolFrequency :
    			entry.getValue().entrySet()) {
    		Double frequency = protocolFrequency.getValue();
    		if (frequency < frequencyThreshold) {
    			continue;
    		}

    		String protocol = protocolFrequency.getKey();
    		Map<String, Double> weightedTerm = protocolMap.get(protocol);
    		if (weightedTerm  == null) {
    			weightedTerm = new HashMap<String, Double>();
    			protocolMap.put(protocol, weightedTerm);
    		}

    		weightedTerm.put(term,
    				Math.pow(frequency / sumOfFrequencies, rho));
    	}
    }
    return protocolMap;
  }

}
