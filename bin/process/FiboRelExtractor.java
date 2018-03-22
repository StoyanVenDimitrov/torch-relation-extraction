/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.FileOutputStream;
import java.io.*;

import org.apache.jena.rdf.model.*;
import org.apache.jena.util.FileManager;
import org.apache.jena.vocabulary.*;
import org.apache.jena.query.* ;


import java.io.*;


public class FiboRelExtractor extends Object {
    
    static final String inputFileName = "fibo-vP.ttl";
    
    public static void main (String args[]) throws IOException {
        // create an empty model
        Model model = ModelFactory.createDefaultModel();
       	FileOutputStream out=null;
	File file;
        // use the FileManager to find the input file
        InputStream in = FileManager.get().open(inputFileName);
        if (in == null) {
            throw new IllegalArgumentException( "File: " + inputFileName + " not found");
        }
        
        // read the RDF/XML file
       	model.read(new FileInputStream(inputFileName),null,"TTL");
	String queryString = "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>" +
		 	     "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" +
		 	     "PREFIX dct:  <http://purl.org/dc/terms/>" +
 			     "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" +
 			     "PREFIX owl:  <http://www.w3.org/2002/07/owl#>" +
			     "SELECT ?concept ?predicat ?object " +
			     "WHERE {?concept rdf:type skos:Concept." +
     			     "?concept ?predicat ?object"+
			     "}" 
			     ;

   	Query query = QueryFactory.create(queryString) ;
 	QueryExecution qexec = QueryExecutionFactory.create(queryString, model);
      	ResultSet results = qexec.execSelect() ;
      	results = ResultSetFactory.copyResults(results) ;
  	
    	try {
		file = new File("fiboProdTriples.tsv");
		out = new FileOutputStream(file);
		ResultSetFormatter.outputAsTSV(out, results);

	} catch (FileNotFoundException fnfe) {
        System.out.println(fnfe);
    	}

    }
}
