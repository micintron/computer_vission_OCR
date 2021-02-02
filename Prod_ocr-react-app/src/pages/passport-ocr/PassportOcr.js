import React from 'react';
import './PassportOcr.scss';
import UploadService from '../../services/Upload';
import FileInput from '../../views/file-input/FileInput';
import LoadingOverlay from '../../views/loading-overlay/LoadingOverlay';

class PassportOcr extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            uploadService: new UploadService()
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

        let ocr = {url: URL.createObjectURL(file), file: file, passport: await this.state.uploadService.passportAnalysis(file)};

        this.setState({
            ocr: ocr,
            loading: false
        })
    }

    render() { 

        console.log(this.state);

        return (

            <div className="passport-ocr-page-container">

                <div className={['passport-file-input-container', this.state.ocr ? 'hide' : ''].join(' ')}>
                    <FileInput fileChangedCallback={this.fileChanged} accept="image/*">Click or Drag to Upload <br /> a Passport Image</FileInput> 
                    
                    <div className={['passport-loading-overlay-container', !this.state.loading ? 'hide' : ''].join(' ')}>
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

                            <div className="ocr-passport-container">
                                <div className="field-container">
                                    <div className="name">Last Name</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.last_name : ''}</div>
                                </div>

                                <div className="field-container">
                                    <div className="name">First Name</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.first_name : ''}</div>
                                </div>

                                <div className="field-container">
                                    <div className="name">Country</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.country : ''}</div>
                                </div>

                                <div className="field-container">
                                    <div className="name">Country Code</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.country_code : ''}</div>
                                </div>

                                <div className="field-container">
                                    <div className="name">Nationality</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.nationality : ''}</div>
                                </div>

                                <div className="field-container">
                                    <div className="name">Sex</div>
                                    <div className="value">{this.state.ocr ? this.state.ocr.passport.sex : ''}</div>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        )
    }
}

export default PassportOcr;