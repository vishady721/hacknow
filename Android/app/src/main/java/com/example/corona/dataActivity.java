package com.example.corona;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.JSONArrayRequestListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import okhttp3.OkHttpClient;

public class dataActivity extends AppCompatActivity {
    TextView tv;
    JSONObject responseObject;
    String text;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_data);

        tv = findViewById(R.id.textView);



        AndroidNetworking.initialize(getApplicationContext());

        DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
        final String date = df.format(Calendar.getInstance().getTime());

        String link = "https://api.covid19api.com/total/country/" +
                "united-states/status/confirmed?from=2020-03-01T00:00:00Z&to=" +date;



        AndroidNetworking.get(link)
                .setPriority(Priority.MEDIUM)
                .build()
                .getAsJSONArray(new JSONArrayRequestListener() {
                    @Override
                    public void onResponse(JSONArray response) {
                        // do anything with response

                        try {
                            responseObject = response.getJSONObject(response.length()-1);
                            String numberOfCases = responseObject.get("Cases").toString();
                            tv.setText("CURRENTLY " +numberOfCases +" COVID CASES IN YOUR COUNTRY");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        Log.v("myTag", "Response completed " +responseObject.toString());
                    }
                    @Override
                    public void onError(ANError error) {
                        // handle error
                        Log.v("myTag", "Error " +error.toString());

                    }
                });



        String link2 = "https://api.covid19api.com/live/country/united-states/status/confirmed";



        AndroidNetworking.get(link2)
                .setPriority(Priority.MEDIUM)
                .build()
                .getAsJSONArray(new JSONArrayRequestListener() {
                    @Override
                    public void onResponse(JSONArray response) {
                        // do anything with response
                        try {


                         for(int i = response.length() - 1; i>0; i-- ){
                            if(response.getJSONObject(i).get("Province").toString().equals("California")){
                                responseObject = response.getJSONObject(i);
                                String confirmedCases = responseObject.get("Confirmed").toString();
                                String deaths = responseObject.get("Deaths").toString();
                                String recovered = responseObject.get("Recovered").toString();

                                text = "IN CALIFORNIA: \n There are currently " +confirmedCases + " confirmed cases. \n \n \n" +
                                        " There are currently " +deaths +" deaths. \n \n \n " +
                                        " There are currently " +recovered +" recovered patients \n \n \n " +
                                        " \n \n \n INFORMATION RETRIEVED JUST NOW, AT : " +date +
                                        "\n \n \n DATA RECEIVED FROM POSTMAN"   ;

                                break;
                            }
                        }


                            tv.append("\n \n " +text);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        Log.v("myTag", "Response completed " +responseObject.toString());
                    }
                    @Override
                    public void onError(ANError error) {
                        // handle error
                        Log.v("myTag", "Error " +error.toString());

                    }
                });

    }
}
