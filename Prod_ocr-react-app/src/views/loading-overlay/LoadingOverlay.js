import React from 'react';
import './LoadingOverlay.scss';

class LoadingOverlay extends React.Component {

    constructor(props) {

        super(props);

        this.state = {

        }
    }

    render() {

        return (
            <div className="loading-overlay">
                <div className="lds-ellipsis">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
        );
    }

}

export default LoadingOverlay;