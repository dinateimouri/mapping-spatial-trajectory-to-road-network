# mapping-spatial-trajectory-to-road-network
This repository provides an implementation for matching spatial trajectory data from the Geolife dataset (specifically, the city of Beijing) to a road network using the Leuven Map-Matching algorithm. The Leuven Map-Matching algorithm is known for its ability to handle noisy and sparse GPS data effectively. It employs a Hidden Markov Model (HMM) with non-emitting states, which assumes that the underlying system follows a Markov process.

To improve the accuracy of the map-matching algorithm, the searching distance radius has been set to 50 meters. This value is determined based on the estimated road widths in Beijing, which typically range from 10 to 40 meters, as well as the standard deviation of GPS noise, which is approximately 4 meters. By considering these factors, the map-matching parameters have been adapted to the specific characteristics of the dataset and the road network.

The output of the map matching process is a sequence of OpenStreetMap (OSM) nodes that represent the user's traversal along the road network. 

