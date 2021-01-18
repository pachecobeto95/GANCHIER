import cv2

class DescriptorsMatcher:
    """
    Class for matching a discriptor vectors against dataset samples 
    Recommended constructor parameters:
    FLANN_MAX_DISTANCE=33
    FLANN_MIN_FREQUENCY=3
    FLANN_INDEX_PARAMS=dict(algorithm = 6,
                    table_number = 6, 
                    key_size = 12,     
                    multi_probe_level = 2) 
    FLANN_SEARCH_PARAMS=dict(checks=200)
    """

    def __init__(self,max_distance,min_frequency, index_params, search_params):
        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.max_distance = max_distance
        self.min_frequency = min_frequency
        self.cache_size = 0
        self.labels = []
    
    def add(self, labeled_descriptors):
        '''
        Inserts feature vectors of an image to train the matcher
        Input:
        labeled_descriptors: list(optional) of tuples (descriptors, label: string)
        '''
        if not isinstance(labeled_descriptors, list):
            labeled_descriptors = [labeled_descriptors]

        for (i,l) in labeled_descriptors:
            self.labels.append(l)
            self.flann.add([i])
            self.cache_size +=1
    
    def train(self):
        '''
        Trains the matcher, not necessary, but improves matching delay
        '''
        self.flann.train()
   
    def flush(self):
        '''
        Clears the matcher
        '''
        self.flann.clear()
        self.cache_size = 0
        self.labels = []
    
    def match(self,query):
        '''
        matches the query against the dataset
        Input:
        query: descriptor vector
        
        Output:
        list of labels of the matched images
        '''
        matches = self.__match(query)
        results = self.__read_matches(matches)
        processed_results = self.__process_results(results)
        labels = self.__get_labels(processed_results)
        return labels
    
    def __match(self, query):
        matches = self.flann.knnMatch(query,10*self.cache_size)
        return matches
    
    def __read_matches(self, matches):
        result = {} #the key of the dict will be the training image index, 
                    #and the value a list [sum of distances, number of matches]
        for match_list in matches:
            for m in match_list:
                if m.distance <= self.max_distance: #filter matches 
                    if m.imgIdx in result:
                        result[m.imgIdx][0] += m.distance
                        result[m.imgIdx][1] += 1
                    else:
                        result[m.imgIdx] = [m.distance,1] 
        return result
    
    def __process_results(self, result):
        for k,v in list(result.items()):
            if v[1] < self.min_frequency:
                del result[k]
            else:
                result[k][0] /= result[k][1] #normalize the distance value (divide by number of matches)
        return result
    
    def __get_labels(self, result):
        #return the labels of the images ordered by avg dist
        return [self.labels[k] for k,_ in sorted(result.items(), key=lambda item: item[1][0])]
    



            
