
class UploadService {

    passportAnalysis(file){

        return new Promise((resolve) => {

            let formData = new FormData();

            formData.append('imagefile', file);

            fetch("http://localhost:5000/passport", 
                {
                    method: 'POST',
                    body: formData
                })
                .then(res => res.json())
                .then(
                    (data) => {        
                        
                        resolve(data)
                    },
                    (error) => {
                        resolve({})
                    }
                )

        })
    }

    licenseAnalysis(file){

        return new Promise((resolve) => {

            let formData = new FormData();

            formData.append('imagefile', file);

            fetch("http://localhost:5000/drivers_license", 
                {
                    method: 'POST',
                    body: formData
                })
                .then(res => res.json())
                .then(
                    (data) => {        
                        
                        resolve(data)
                    },
                    (error) => {
                        resolve(null);
                        /*
                        setTimeout(() => {
                            resolve({
                                "CLASS": "CLASS: A",
                                "DD": "5 00:123567890123",
                                "DLN": "CDL",
                                "DOB": "D0B: 08/04/1975",
                                "DUPS": "DUPS: 00",
                                "EXP": "4B EXP: 08/05/2023",
                                "EYES": "8 EYES: BRO",
                                "HGT": "16 HGT: 5'-06\"",
                                "SEX": "5 SEX: F",
                                "personal_info": [
                                    "COMMERCIAL",
                                    "PENNSYLVANA",
                                    "DRIVER'S LICENSE",
                                    "YIST PI COM",
                                    "US4",
                                    "AD DLN: 99 999 999",
                                    "DUPS: 00",
                                    "D0B: 08/04/1975",
                                    "4B EXP: 08/05/2023",
                                    "4A|SS: 03/01/2019",
                                    "SAMPLE",
                                    "2 JANICE ANN",
                                    "8 123 MAIN STREET",
                                    "AARRISBURG, PA 17101-0000",
                                    "8 EYES: BRO",
                                    "5 SEX: F",
                                    "16 HGT: 5'-06\"",
                                    "CLASS: A",
                                    "9A ENND: NONE",
                                    "CDL",
                                    "A2RESTR: NONE",
                                    "DAMICE TJAMPLE",
                                    "5 00:123567890123",
                                    "456789012345",
                                    "ORGAN DONOR"
                                ]
                               })
                        }, 1000)
                        */
                    }
                )

        })
    }

    ocrAnalysis(file) {

        return new Promise((resolve) => {

            let formData = new FormData();

            formData.append('imagefile', file);

            fetch("http://localhost:5000/image", 
                {
                    method: 'POST',
                    body: formData
                })
                .then(res => res.json())
                .then(
                    (data) => {        
                        
                        resolve(data)
                    },
                    (error) => {
                        resolve(null)
                    }
                )

        })
    }

    sentimentAnalysis(value) {

        return new Promise((resolve) => {

            fetch("http://localhost:5000/nlp_sa", 
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({words: [value]})
                })
                .then(res => res.json())
                .then(
                    (data) => {        
                        console.log(data);
                        resolve({scores: [data.scores[0][1][0]]})
                    },
                    (error) => {

                        resolve(null)
                        console.log(error)
                    }
                )

        })
    }

    summaryAnalysis(value) {

        return new Promise((resolve) => {

            fetch("http://localhost:5000/simple_summary", 
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({text: value})
                })
                .then(res => res.json())
                .then(
                    (data) => {        
                        
                        resolve({summary: data.summary_text || value})
                    },
                    (error) => {

                        setTimeout(() => {
                            resolve({"summary": value})
                        }, 1000)
                        
                    }
                )

        })
    }
}

export default UploadService;