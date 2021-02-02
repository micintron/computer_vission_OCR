import React from 'react';
import './PdfOcr.scss';
import UploadService from '../../services/Upload';
import * as pdfjsLib from 'pdfjs-dist/build/pdf';
import FileInput from '../../views/file-input/FileInput';
import LoadingOverlay from '../../views/loading-overlay/LoadingOverlay';
import TextAnalysisOutput from '../../views/text-analysis-output/TextAnalysisOutput';

class PdfOcr extends React.Component {
 
    constructor(props) {

        pdfjsLib.GlobalWorkerOptions.workerSrc = '/workers/pdf.worker.js';

        super(props);
        
        this.state = {
            uploadService: new UploadService(),
            pdfImages: null
        }
        
        this.fileChanged = this.fileChanged.bind(this);
        this.resetPage = this.resetPage.bind(this);
    }

    resetPage() {

        this.setState({
            pdfImages: null
        })
    }

    async fileChanged(file) {

        this.setState({
            loading: true
        })

        let pdfImages = await this.convertPdfToImages(file);

        for(let pdfImage of pdfImages) {

            let pdfText = await this.state.uploadService.ocrAnalysis(pdfImage.file);

            let summaryRes = await this.state.uploadService.summaryAnalysis(pdfText);
            let summarySentiment = await this.state.uploadService.sentimentAnalysis(summaryRes.summary);

            pdfImage.textOutput = {
                summary: {
                    text: summaryRes.summary,
                    sentiment: summarySentiment.scores[0]
                },
                original: {
                    text: pdfText
                }
            };
        }

        this.setState({
            pdfImages: pdfImages,
            loading: false
        })
    }

    async getPage(pdf, pageNum) {

        return new Promise(res => {

            let canvas = document.createElement('canvas');

            pdf.getPage(pageNum).then((page) => {

                let scale = 1.5;
                let viewport = page.getViewport({ scale: scale });

                let context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                let renderContext = {
                    canvasContext: context,
                    viewport: viewport,
                };

                let pageRendering = page.render(renderContext);

                var completeCallback = pageRendering._internalRenderTask.callback;

                pageRendering._internalRenderTask.callback = (error) => {

                    completeCallback.call(this, error);

                    let base64Img = canvas.toDataURL("image/jpeg", 1);

                    res({image: base64Img, file: this.dataURItoBlob(base64Img), text: null});
                };

            });
        });
    }

    async loadPdf(url) {

        return new Promise(res => {

            let loadingTask = pdfjsLib.getDocument(url);

            loadingTask.promise.then((pdf) => {
    
                res(pdf)
            });
        });
    }

    async convertPdfToImages(file) {
        
        let pageImages = [];

        let pdf = await this.loadPdf(URL.createObjectURL(file))

        for(let i = 1; i <= pdf.numPages; i++) {

            pageImages.push(await this.getPage(pdf, i));
        }

        return new Promise(res => {

            res(pageImages)
        });
    }

    dataURItoBlob(dataURI) {
        // convert base64/URLEncoded data component to raw binary data held in a string
        let byteString;
        if (dataURI.split(',')[0].indexOf('base64') >= 0)
            byteString = atob(dataURI.split(',')[1]);
        else
            byteString = unescape(dataURI.split(',')[1]);
        // separate out the mime component
        var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        // write the bytes of the string to a typed array
        var ia = new Uint8Array(byteString.length);
        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ia], {type:mimeString});
    }

    generatePdfHtml() {

        if(this.state.pdfImages) {

            let response = [];

            for(let pdfImage of this.state.pdfImages) {

                response.push(

                    <div className="file-output-state-content-container">

                        <div className="ocr-image-container">

                            <div className="ocr-image-wrapper">
                                <img className="ocr-image" src={pdfImage.image} />
                            </div>

                            <div class="ocr-text-container">
                                <TextAnalysisOutput output={pdfImage.textOutput} />
                            </div>
                        </div>
                        
                    </div>

                )
            }

            return response;
        }

        return '';
    }

    render() { 

        console.log(this.state);

        return (

            <div className="pdf-ocr-page-container">

                <div className={['pdf-file-input-container', this.state.pdfImages ? 'hide' : ''].join(' ')}>

                    <FileInput fileChangedCallback={this.fileChanged} accept="application/pdf">Click or Drag to Upload <br /> a PDF File</FileInput> 

                    <div className={['pdf-loading-overlay-container', !this.state.loading ? 'hide' : ''].join(' ')}>
                        <LoadingOverlay />
                    </div>
                </div>

                <div className={['file-output-state-container', !this.state.pdfImages ? 'hide' : ''].join(' ')}>

                    <button onClick={this.resetPage}>Upload New File</button>

                    {this.generatePdfHtml()}
                </div>
            </div>
        )
    }
}

export default PdfOcr;