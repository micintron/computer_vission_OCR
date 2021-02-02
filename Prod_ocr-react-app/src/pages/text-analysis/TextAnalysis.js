import React from 'react';
import './TextAnalysis.scss';
import UploadService from '../../services/Upload';
import TextAnalysisOutput from '../../views/text-analysis-output/TextAnalysisOutput';

class TextAnalysis extends React.Component {

    constructor(props) {

        super(props);

        this.state = {
            uploadService: new UploadService(),
            textInput: null,
            textOutput: null
        }

        this.analyzeClicked = this.analyzeClicked.bind(this);
        this.updateTextInputValue = this.updateTextInputValue.bind(this);
    }

    async analyzeClicked() {

        this.setState({
            textOutput: {}
        })

        let summaryRes = await this.state.uploadService.summaryAnalysis(this.state.textInput);
        let summarySentiment = await this.state.uploadService.sentimentAnalysis(summaryRes.summary);
        let originalSentiment = await this.state.uploadService.sentimentAnalysis(this.state.textInput);

        this.setState({
            textOutput: {
                summary: {
                    text: summaryRes.summary,
                    sentiment: summarySentiment.scores[0]
                },
                original: {
                    text: this.state.textInput,
                    sentiment: originalSentiment.scores[0]
                }
            }
        })
    }

    updateTextInputValue(event) {

        this.setState({
            textInput: event.target.value
        })
    }

    render() { 
        
        return (

            <div className="text-analysis-page-container">

                <div className="text-analysis-page-content-container">

                    <div className="text-input-container">

                        <textarea placeholder="Enter the text you would like to be summarized and analyzed for sentiment..." className="text-input" value={this.state.textInput} onChange={this.updateTextInputValue}></textarea>

                        <button onClick={this.analyzeClicked}>Analyze Text</button>
                    </div>

                    <div className="text-output-container">
                        <TextAnalysisOutput output={this.state.textOutput} />
                    </div>
                </div>
            </div>
        )
    }
}

export default TextAnalysis;