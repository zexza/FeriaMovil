package com.example.feriavirtual


import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.webkit.*
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.*


class MainActivity : AppCompatActivity() {

    private var cargaView = false

    private var navegador:WebView?=null
    private var ulrFeria = "http://192.168.1.15:81/"
    private var urlRestar = "http://192.168.1.15:81/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        navegador=findViewById(R.id.navegador)
        navegador?.clearCache(false)
        navegador?.loadUrl(ulrFeria+"login/")
        cargaView = false

        navegador?.webChromeClient = object : WebChromeClient(){
        }
        navegador?.webViewClient = object : WebViewClient(){
        }
        navegador?.isInvisible = false


        navegador?.webViewClient = object : WebViewClient(){

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                navegador?.isInvisible = true

                super.onReceivedError(view, request, error)
                cargaView = true
                Toast.makeText(this@MainActivity,"error al cargar: $error", Toast.LENGTH_LONG).show()

            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                if (cargaView == true){


                }else{
                    navegador?.isInvisible = false
                }

            }

        }


    }




    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.nav_menu,menu)
        return super.onCreateOptionsMenu(menu)
    }


    fun backButton2(){
        cargaView = false
        if (navegador?.canGoBack() == true){
            navegador?.goBack();

        }else {
            super.onBackPressed();
        }
    }


    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when(item.itemId){
            R.id.id_info -> moreInfo()
            R.id.id_back -> backButton2()
            R.id.id_restart2 -> recargar()
            R.id.id_restart -> cargar()
        }
        return super.onOptionsItemSelected(item)
    }


    fun moreInfo(){
        cargaView = false

        navegador?.clearCache(false)
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl("https://drive.google.com/drive/folders/1YmE9M90BfGtPuC2hsz3wREhQa3-v8tQw?usp=share_link")


    }
    fun recargar(){
        cargaView = false


        urlRestar = navegador?.url.toString()
        navegador?.clearCache(false)
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl(urlRestar)



    }

    fun cargar(){
        cargaView = false

        navegador?.clearCache(false)
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl(ulrFeria)



    }



}