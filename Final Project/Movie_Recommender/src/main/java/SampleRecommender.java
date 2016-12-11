import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import java.io.File;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.neighborhood.*;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.recommender.*;

import java.io.IOException;
import java.util.List;
import java.util.*;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;



class SampleRecommender {
    public static void main(String [] args) throws TasteException, IOException {
        DataModel model = new FileDataModel(new File("ratings.csv"));
        UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
        UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1, similarity, model);
        UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);

        Boolean wantToContinue = true;
        //Note - change this to correct filepath
        HashMap<Integer,String> movieMap = mapMovieToID("movies.csv");
        do {
            System.out.print("What user id would you like recomendations for?");
            Scanner scan = new Scanner(System.in);
            int userID=scan.nextInt();

            System.out.print("How many recommendations would you like?");
            int numRecommendations=scan.nextInt();

            List recommendations = recommender.recommend(userID, numRecommendations);
            for (Object recommendation : recommendations) {
                String recommendationString = recommendation.toString();
                String movieID = recommendationString.substring(21,Str.indexOf(','));
                String rating = recommendationString.substring(Str.indexOf(',') + 8,Str.indexOf(',') + 8);
                System.out.println(map.get(Integer.parseInt(movieID)) + ", rating: " + rating);
            }

            System.out.print("Do you want to continue? (y/n)");
            String continueString = scan.next();
            wantToContinue = continueString.equals("y") || continueString.equals("Y");
        } while (wantToContinue);

    }

    public static HashMap<Integer,String> mapMovieToID(String csvFile) {
        HashMap<Integer,String> map = new HashMap<Integer,String>();
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] lineData = line.split(cvsSplitBy);
                map.put(Integer.parseInt(lineData[0]),lineData[1]);

            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return map;
    }
}