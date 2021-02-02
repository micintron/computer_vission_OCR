import React from 'react';
import './LicenseOcr.scss';
import UploadService from '../../services/Upload';
import FileInput from '../../views/file-input/FileInput';
import LoadingOverlay from '../../views/loading-overlay/LoadingOverlay';
import { fireEvent } from '@testing-library/react';

class LicenseOcr extends React.Component {

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

        let ocr = {url: URL.createObjectURL(file), file: file, license: await this.state.uploadService.licenseAnalysis(file)};

        this.setState({
            ocr: ocr,
            loading: false
        })
    }
    /*
    parseLicenseResponse(response) {
        console.log(response);

        let name = null;
        let address = null;
        let state = null;
        let licenseClass = null;
        let sex = null;
        let height = null;
        let eyes = null;
        let dob = null;
        let exp = null;

        try { name = response[11].replaceAll("2", "").trim() } catch(e){}
        try { address = response[12].replaceAll("8", "").trim() + ", " + response[13] } catch(e){}
        try { state = response[1] } catch(e){}
        try { licenseClass = response[18].split(":")[1].trim() } catch(e){}
        try { sex = response[16].split(":")[1].trim() } catch(e){}
        try { height = response[17].split(":")[1].trim() } catch(e){}
        try { eyes = response[15].split(":")[1].trim() } catch(e){}
        try { dob = response[7].split(":")[1].trim() } catch(e){}
        try { exp = response[8].split(":")[1].trim() } catch(e){}

        return {
            name: name,
            address: address,
            state: state,
            class: licenseClass,
            sex: sex,
            height: height,
            eyes: eyes,
            dob: dob,
            exp: exp
        }
    }
    */

    generateLicenseHtml(license) {

        let fields = [];

        if(license) {

            for(let i in license) {

                let item = license[i];

                if(!Array.isArray(item)) {

                    fields.push(
                        <div className="field-container">
                            <div className="name">{i}</div>
                            <div className="value">{item}</div>
                        </div> 
                    )
                }
            }
        }

        return fields;
    }

    generateLicenseAdditionalHtml(license) {

        let fields = [];

        if(license) {

            for(let i in license) {

                let item = license[i];

                if(Array.isArray(item)) {

                    for(let j = 0; j < item.length; j++) {

                        let subItem = item[j];

                        fields.push(
                            <div className="field-container">
                                <div className="value">{subItem}</div>
                            </div> 
                        )
                    }
                }
            }
        }

        return fields;
    }

    render() { 
        
        return (

            <div className="license-ocr-page-container">

                <div className={['license-file-input-container', this.state.ocr ? 'hide' : ''].join(' ')}>

                    <FileInput fileChangedCallback={this.fileChanged} accept="image/*">Click or Drag to Upload <br /> a Drivers License</FileInput> 
                    
                    <div className={['license-loading-overlay-container', !this.state.loading ? 'hide' : ''].join(' ')}>
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

                            <div className="ocr-license-container">
                                {this.generateLicenseHtml(this.state.ocr ? this.state.ocr.license : null)}
                            </div>
                        </div>
                        
                        <div className="ocr-additional-container">
                            <div className="label">Additional Fields</div>
                            <div className="ocr-additional-content-container">
                                {this.generateLicenseAdditionalHtml(this.state.ocr ? this.state.ocr.license : null)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default LicenseOcr;