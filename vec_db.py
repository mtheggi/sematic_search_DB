
from kdtree import *
import kdtree
import csv
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity



class VecDB(object):

    def __init__(self, file_path="None", new_db=True,small_db_size=0) -> None:
        self.file_path = file_path
        self.new_db = new_db
        self.small_db_size=small_db_size
        # lstcnt check 

    def insert_records(self, records: list[dict]) -> None:
        if self.new_db == True: #creat a new_database
            self.small_db_size+=len(records)
            with open("small_database.csv", 'w', newline='') as csvfile:
                print("records size = " , len(records) )
                print(self.small_db_size)
                writer = csv.writer(csvfile)
                for item in records:
                    vectorID = item["id"]
                    value = item["embed"]
                    if(len(value) != 70):
                        print("error: vector size is not 70")
                    writer.writerow([vectorID, *value])
            self.new_db = False
        else:
            self.small_db_size+=len(records)
            print("records size = " , len(records) )
            print(self.small_db_size)
            with open("small_database.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for item in records:
                    vectorID = item["id"]
                    value = item["embed"]
                    if(len(value) != 70):
                        print("error: vector size is not 70")
                    writer.writerow([vectorID, *value])
        
        kdtree.lstcnt=0 
        kdtree.nodes=[]
        kdtree.Internalnodes=[]
        kdtree.ClusterCnt=0
      
      
        createExternalPart('small_database.csv', size=self.small_db_size, dimensions=70, axis=0, sel_axis=None, lstCount=kdtree.lstcnt)
        NodeSerializer.serialize_to_csv(kdtree.nodes, 'small_database_output.csv')
        
        print(lstcnt)
        print("node array size , " , len(nodes))
        self.file_path = 'small_database_output.csv' # serilized file of output database 
      
        
        print("records inserted and serilized successfully")
        return 
        

    def retrive(self, query , topk)->list : # return list of ids 
        
        #file_path = test_1m_z/test_1m_d/output.csv
        parentDir= ""
        if self.small_db_size == 0 :
            parentDir = self.file_path[:(len(self.file_path)-10)]

        Ids=[]
        resultTuple= search_knn(self.file_path, query.tolist()[0], topk ,  dist=kdtree.distance , parentDirectory=parentDir) # return (node, distance) 
        for i in resultTuple:
            Ids.append(i[0].id)
        return Ids

            
            

# path= "test_1m_z/test_1m_d/output.csv"

# print(path[:(len(path)-10)])



# QUERY_SEED_NUMBER = 200
# DB_SEED_NUMBER = 50

# db = VecDB('test_1m_z/test_1m_d/output.csv' , new_db=False)

# rng = np.random.default_rng(DB_SEED_NUMBER)
# vectors = rng.random((10**6, 70), dtype=np.float32)

# rng = np.random.default_rng(QUERY_SEED_NUMBER)
# query = rng.random((1, 70), dtype=np.float32)
# actual_sorted_ids_10k = np.argsort(vectors.dot(query.T).T / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query)), axis= 1).squeeze().tolist()[::-1]

# # records_dict = [{"id": i, "embed": list(row)} for i, row in enumerate(vectors)]
# # db.insert_records(records_dict)
# ids = db.retrive(query, 10)
# print(actual_sorted_ids_10k[:10])
# print(ids)


         
