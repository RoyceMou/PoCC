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



class SampleRecommender {
    public static void main(String [] args) throws TasteException, IOException {
        DataModel model = new FileDataModel(new File("ratings.csv"));
        UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
        UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1, similarity, model);
        UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);

        Boolean wantToContinue = true;
        do {
            System.out.print("What user id would you like recomendations for?");
            Scanner scan = new Scanner(System.in);
            int userID=scan.nextInt();

            System.out.print("How many recommendations would you like?");
            int numRecommendations=scan.nextInt();

            List recommendations = recommender.recommend(userID, numRecommendations);
            for (Object recommendation : recommendations) {
                System.out.println(recommendation);
            }

            System.out.print("Do you want to continue? (y/n)");
            String continueString = scan.next();
            wantToContinue = continueString.equals("y") || continueString.equals("Y");
        } while (wantToContinue);

    }
}