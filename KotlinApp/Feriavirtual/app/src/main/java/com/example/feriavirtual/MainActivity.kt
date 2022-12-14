package com.example.feriavirtual


import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.view.Menu
import android.view.MenuItem
import android.webkit.*
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.*


class MainActivity : AppCompatActivity() {

    private var cargaView = false
    private var progressBar1:ProgressBar?=null
    private var navegador:WebView?=null
    private var textReconectar:TextView?=null
    private var ulrFeria = "http://192.168.1.15:81/"
    private var urlRestar = "http://192.168.1.15:81/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        navegador=findViewById(R.id.navegador)
        progressBar1 = findViewById(R.id.id_progess)
        textReconectar = findViewById(R.id.textView2)

        navegador?.loadUrl(ulrFeria+"login1/")
        cargaView = false
        textReconectar?.isInvisible = true
        navegador?.webChromeClient = object : WebChromeClient(){
        }
        navegador?.webViewClient = object : WebViewClient(){
        }
        navegador?.isInvisible = false



        navegador?.webViewClient = object : WebViewClient(){


            override fun onLoadResource(view: WebView?, url: String?) {
                if (navegador?.url.toString() == "http://192.168.1.15:81/login1/") {
                }
                else{
                    super.onLoadResource(view, url)
                    navegador?.isInvisible = true
                    progressBar1?.isInvisible = false
                    textReconectar?.isInvisible = true
                }
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                textReconectar?.isInvisible = false
                navegador?.isInvisible = true
                navegador?.isInvisible = true
                super.onReceivedError(view, request, error)
                cargaView = true
                Toast.makeText(this@MainActivity,"error al cargar", Toast.LENGTH_LONG).show()

            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                if (navegador?.url.toString() == "http://192.168.1.15:81/login1/"){
                    navegador?.loadUrl ("http://192.168.1.15:81/login/")
                }
                if (cargaView == true){


                }else{
                    progressBar1?.isInvisible = true
                    navegador?.isInvisible = false
                }

            }




        }


        navegador?.setDownloadListener(DownloadListener {
                url,
                userAgent,
                contentDescription,
                mimetype,
                contentLength ->

            // Initialize download request
            val request = DownloadManager.Request(Uri.parse(url))

            // Get the cookie
            val cookies = CookieManager.getInstance().getCookie(url)

            // Add the download request header
            request.addRequestHeader("Cookie",cookies)
            request.addRequestHeader("User-Agent",userAgent)

            // Set download request description
            request.setDescription("Downloading requested file....")

            // Set download request mime tytpe
            request.setMimeType(mimetype)

            // Allow scanning
            request.allowScanningByMediaScanner()

            // Download request notification setting
            request.setNotificationVisibility(
                DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)

            // Guess the file name
            val fileName = URLUtil.guessFileName(url, contentDescription, mimetype)

            // Set a destination storage for downloaded file
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName)

            // Set request title
            request.setTitle(URLUtil.guessFileName(url, contentDescription, mimetype));


            // DownloadManager request more settings
            request.setAllowedOverMetered(true)
            request.setAllowedOverRoaming(false)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                request.setRequiresCharging(false)
                request.setRequiresDeviceIdle(false)
            }
            request.setVisibleInDownloadsUi(true)


            // Get the system download service
            val dManager = getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager

            // Finally, request the download to system download service
            dManager.enqueue(request)
        })









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

        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl("https://drive.google.com/drive/folders/1YmE9M90BfGtPuC2hsz3wREhQa3-v8tQw?usp=share_link")


    }
    fun recargar(){
        cargaView = false


        urlRestar = navegador?.url.toString()
        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl(urlRestar)



    }

    fun cargar(){
        cargaView = false

        navegador?.settings?.javaScriptEnabled=true
        navegador?.loadUrl(ulrFeria)



    }



}