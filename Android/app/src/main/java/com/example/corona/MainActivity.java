package com.example.corona;

import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.material.navigation.NavigationView;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener{

    DrawerLayout drawer;
    ActionBarDrawerToggle toggle;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        Toolbar myToolbar = (Toolbar) findViewById(R.id.my_toolbar);
        myToolbar.setTitle("");

        setSupportActionBar(myToolbar);


        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);

        toggle = new ActionBarDrawerToggle(
                this, drawer, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        toggle.syncState(); //Syncs drawer state with listener

        NavigationView navigationView = (NavigationView) findViewById(R.id.actualNavigation);
        navigationView.setNavigationItemSelectedListener(this);
    }

    public void volunteerClicked(View v){
        Intent i = new Intent(MainActivity.this, volunteer.class );
        startActivity(i);
    }
    public void seniorClicked(View v){
        Intent i = new Intent(MainActivity.this, requester.class );
        startActivity(i);
    }


    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
        int id = menuItem.getItemId();
        if (id == R.id.liveUpdates) {
            startActivity(new Intent(MainActivity.this, dataActivity.class));
        }

        if (id == R.id.resources) {
            startActivity(new Intent(MainActivity.this, resourcesActivity.class));
        }

        if (id == R.id.seniors) {
            startActivity(new Intent(MainActivity.this, senior.class));
        }

        if (id == R.id.groceries) {
            startActivity(new Intent(MainActivity.this, groceries.class));
        }

        return false;
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        // Sync the toggle state after onRestoreInstanceState has occurred.
        toggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        toggle.onConfigurationChanged(newConfig);
    }
}
