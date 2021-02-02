import React from 'react';
import './TextAnalysisOutput.scss';
import LoadingOverlay from '../loading-overlay/LoadingOverlay';

class TextAnalysisOutput extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            selectedItem: 'original'
        }

        this.navItemClicked = this.navItemClicked.bind(this);
    }
    
    navItemClicked(item) {

        this.setState({
            selectedItem: item
        })
    }

    render() {
        
        return (

            <div className={['text-analysis-output-container', !this.props.output ? 'hide' : ''].join(' ')}> 
                
                <div className="controls-container">
                    <div className={['item', this.state.selectedItem === 'original' ? 'selected' : ''].join(' ')} onClick={() => this.navItemClicked('original')}>Original</div>
                    <div className={['item', this.state.selectedItem === 'summary' ? 'selected' : ''].join(' ')} onClick={() => this.navItemClicked('summary')}>Summary</div>
                </div>

                <div className={['output-container', this.state.selectedItem !== 'original' ? 'hide' : ''].join(' ')}>

                    <div className="output-text-wrapper">

                        <div className={['sentiment-score-container',  !this.props.output || !this.props.output.original || !this.props.output.original.sentiment ? 'hide' : ''].join(' ')}>
                            <span>Sentiment Score:</span> <span className={['score-value', this.props.output && this.props.output.original &&  this.props.output.original.sentiment &&  this.props.output.original.sentiment.label === 'POSITIVE' ? 'green' : 'red'].join(' ')}>{this.props.output && this.props.output.original && this.props.output.original.sentiment ? this.props.output.original.sentiment.label + " " + (this.props.output.original.sentiment.score * 100).toFixed(2) : ''}</span>
                        </div>

                        <div className="text-container">
                            {this.props.output && this.props.output.original ? this.props.output.original.text : ''}
                        </div>

                        <div className={['loading-overlay-wrapper', this.props.output && this.props.output.original ? 'hide' : ''].join(' ')}>
                            <LoadingOverlay />
                        </div>
                    </div>
                </div>

                <div className={['output-container', this.state.selectedItem !== 'summary' ? 'hide' : ''].join(' ')}>

                    <div className="output-text-wrapper">

                        <div className="sentiment-score-container">
                            <span>Sentiment Score:</span> <span className={['score-value', this.props.output && this.props.output.summary &&  this.props.output.summary.sentiment.label === 'POSITIVE' ? 'green' : 'red'].join(' ')}>{this.props.output && this.props.output.summary ? this.props.output.summary.sentiment.label + " " + (this.props.output.summary.sentiment.score * 100).toFixed(2) : ''}</span>
                        </div>

                        <div className="text-container summary">
                            {this.props.output && this.props.output.summary ? this.props.output.summary.text : ''}
                        </div>

                        <div className={['loading-overlay-wrapper', this.props.output && this.props.output.summary ? 'hide' : ''].join(' ')}>
                            <LoadingOverlay />
                        </div>
                    </div>
                </div>
            </div>
            
        );
    }

}

export default TextAnalysisOutput;