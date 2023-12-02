import React from "react";
import ReactFileReader from "react-file-reader";
import Papa from "papaparse";

import "./App.css";

function App() {
  const uploadFile = (files) => {
    Papa.parse(files[0], {
      complete: function (results) {
        const eegData = results.data.slice(2);
        const attentionScores = eegData.map(
          (row) => row[results.data[1].indexOf("PM.Attention.Scaled")]
        );
        const timestamps = eegData.map(
          (row) => row[results.data[1].indexOf("Timestamp")]
        );

        const nonEmptyAttentionIndices = [];
        for (let i = 0; i < attentionScores.length; i++) {
          if (attentionScores[i] !== "") {
            nonEmptyAttentionIndices.push(i);
          }
        }
        const attentionScoresOfNonEmpty = nonEmptyAttentionIndices.map(
          (index) => attentionScores[index]
        );
        const timestampsOfNonEmpty = nonEmptyAttentionIndices.map(
          (index) => timestamps[index]
        );
      },
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>Rewind EEG</p>
        <ReactFileReader handleFiles={uploadFile} fileTypes={".csv"}>
          <button className="btn"> Upload EEG Data</button>
        </ReactFileReader>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
