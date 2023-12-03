import React, { useState, useRef } from "react";
import ReactFileReader from "react-file-reader";
import Papa from "papaparse";
import { Line, getElementAtEvent } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [chartData, setChartData] = useState({});
  const [selectedTimestamp, setSelectedTimestamp] = useState(0);
  const chartRef = useRef();

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
          if (attentionScores[i] && attentionScores[i] !== "") {
            nonEmptyAttentionIndices.push(i);
          }
        }
        const attentionScoresOfNonEmpty = nonEmptyAttentionIndices.map(
          (index) => Number(attentionScores[index]) * 100
        );
        const timestampsOfNonEmpty = nonEmptyAttentionIndices.map((index) =>
          parseInt(Number(timestamps[index]))
        );

        setChartData({
          labels: timestampsOfNonEmpty,
          datasets: [
            {
              label: "Attention Score",
              data: attentionScoresOfNonEmpty,
              fill: false,
              borderColor: "rgba(75,192,192,1)",
              cubicInterpolationMode: "monotone",
              pointRadius: 0,
            },
          ],
        });
      },
    });
  };

  const options = {
    scales: {
      x: {
        type: "linear",
        position: "bottom",
        title: {
          display: true,
          text: "Timestamp",
        },
      },
      y: {
        title: {
          display: true,
          text: "Attention Score",
        },
      },
    },
  };

  const onClick = (event) => {
    if (!getElementAtEvent(chartRef.current, event).length) return;

    setSelectedTimestamp(
      getElementAtEvent(chartRef.current, event)[0]["element"]["$context"][
        "parsed"
      ]["x"]
    );
  };

  return (
    <div className="App">
      <div className="Title">Rewind EEG</div>
      <ReactFileReader handleFiles={uploadFile} fileTypes={".csv"}>
        <button className="btn"> Upload EEG Data</button>
      </ReactFileReader>
      <div className="ChartArea">
        {Object.keys(chartData).length ? (
          <>
            <Line
              ref={chartRef}
              data={chartData}
              options={options}
              onClick={onClick}
            />
          </>
        ) : (
          <></>
        )}
      </div>
      <div className="ScreenshotArea">
        {selectedTimestamp ? <div>Timestamp: {selectedTimestamp}</div> : <></>}
        <img
          className="ScreenshotImage"
          src="/images/2023-12-02 10:11:46.png"
          alt="screenshot"
        />
      </div>
    </div>
  );
}

export default App;
