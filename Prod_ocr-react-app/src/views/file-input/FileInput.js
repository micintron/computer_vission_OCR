import React from 'react';
import './FileInput.scss';
import folder from '../../images/folder.png';

class FileInput extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            fileDragging: false
        }

        this.dragOver = this.dragOver.bind(this);
        this.dragLeave = this.dragLeave.bind(this);
        this.inputChanged = this.inputChanged.bind(this);
    }

    dragOver(e) {

        if(e) {
            e.preventDefault();
            e.stopPropagation();
            e.nativeEvent.stopImmediatePropagation();
        }

        this.setState({
            fileDragging: true
        })
    }

    dragLeave(e) {

        if(e) {
            e.preventDefault();
            e.stopPropagation();
            e.nativeEvent.stopImmediatePropagation();
        }

        this.setState({
            fileDragging: false
        })
    }

    inputChanged(synEvent) {

        let e = synEvent.nativeEvent;

        let file = e.dataTransfer && e.dataTransfer.items ? e.dataTransfer.items[0].getAsFile() : e.srcElement.files[0];

        this.props.fileChangedCallback(file);

        e.srcElement.value = "";

        e.preventDefault();
    }

    render() {

        return (
            
            <div className="file-input-state-container">

                <div className={['file-input-state-content-container', this.state.fileDragging ? 'dragging' : ''].join(' ')} onDragOver={this.dragOver} onDragLeave={this.dragLeave}>

                    <input type="file" onChange={this.inputChanged} accept={this.props.accept} /> 

                    <img className="upload-logo" src={folder} width="150" />

                    <div className="upload-instructions">{this.props.children}</div>

                </div>
            </div>
        );
    }

}

export default FileInput;