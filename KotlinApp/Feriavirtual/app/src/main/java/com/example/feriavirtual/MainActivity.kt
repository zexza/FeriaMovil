package com.example.feriavirtual


import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.KeyEvent
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.appcompat.app.AlertDialog

class MainActivity : AppCompatActivity() {

    private var navegador:WebView?=null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        navegador=findViewById(R.id.navegador)
        navegador?.loadUrl("http://192.168.1.13:81/")
        navegador?.loadUrl("http://192.168.1.15:81/login/")
        navegador?.webChromeClient = object : WebChromeClient(){
        }
        navegador?.webViewClient = object : WebViewClient(){
        }
    }


    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.nav_menu,menu)
        return super.onCreateOptionsMenu(menu)
    }


    fun backButton2(){
        if (navegador?.canGoBack() == true){
            navegador?.goBack();

        }else {
            super.onBackPressed();
        }
    }


    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when(item.itemId){
            R.id.id_back -> backButton2()
            R.id.id_restart -> cargar()
        }
        return super.onOptionsItemSelected(item)
    }


    fun cargar(){
        navegador?.clearCache(false)
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl("http://192.168.1.15:81/")
    }



}