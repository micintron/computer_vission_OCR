import React from 'react';
import './ImageOcr.scss';
import UploadService from '../../services/Upload';
import FileInput from '../../views/file-input/FileInput';
import LoadingOverlay from '../../views/loading-overlay/LoadingOverlay';

class ImageOcr extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            uploadService: new UploadService(),
            ocrImage: null
        }

        this.fileChanged = this.fileChanged.bind(this);
        this.resetPage = this.resetPage.bind(this);
    }

    resetPage() {

        this.setState({
            ocr: null
        })
    }

    async fileChanged(file) {
        
        this.setState({
            loading: true
        })

        let ocr = {url: URL.createObjectURL(file), file: file, text: await this.state.uploadService.ocrAnalysis(file)};

        this.setState({
            ocr: ocr,
            loading: false
        })
    }

    render() { 

        return (

            <div className="image-ocr-page-container">

                <div className={['image-file-input-container', this.state.ocr ? 'hide' : ''].join(' ')}>
                    <FileInput fileChangedCallback={this.fileChanged} accept="image/*">Click or Drag to Upload <br /> an Image File</FileInput> 

                    <div className={['image-loading-overlay-container', !this.state.loading ? 'hide' : ''].join(' ')}>
                        <LoadingOverlay />
                    </div>
                </div>

                <div className={['file-output-state-container', !this.state.ocr ? 'hide' : ''].join(' ')}>

                    <button onClick={this.resetPage}>Upload New File</button>

                    <div className="file-output-state-content-container">

                        <div className="ocr-image-container">

                            <div className="ocr-image-wrapper">
                                <img className="ocr-image" src={this.state.ocr ? this.state.ocr.url : ''} />
                            </div>

                            <div class="ocr-text-container">{this.state.ocr ? this.state.ocr.text : ''}</div>
                        </div>
                        
                    </div>
                </div>
            </div>
        )
    }
}

export default ImageOcr;