package com.example.feriavirtual


import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient

class MainActivity : AppCompatActivity() {

    private var navegador:WebView?=null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        navegador=findViewById(R.id.navegador)
        navegador?.loadUrl("http://192.168.1.13:81/")
        navegador?.loadUrl("http://192.168.1.13:81/")

        navegador?.webChromeClient = object : WebChromeClient(){

        }
        navegador?.webViewClient = object : WebViewClient(){

        }









    }
    fun cargar(view: View){
        navegador?.clearCache(false)
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl("http://192.168.1.13:81/")
    }
}