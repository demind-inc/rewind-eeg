import React, { useState, useRef } from "react";
import ReactFileReader from "react-file-reader";
import Papa from "papaparse";
import dayjs from "dayjs";
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
        const timestampsOfNonEmpty = nonEmptyAttentionIndices.map(
          (index) => parseInt(Number(timestamps[index])) * 1000
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
              pointRadius: 2,
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
          display: false,
          text: "Timestamp",
        },
        ticks: { display: false },
      },
      y: {
        title: {
          display: true,
          text: "Attention Score",
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  const hasEEGData = !!Object.keys(chartData).length;

  const onClick = (event) => {
    if (!getElementAtEvent(chartRef.current, event).length) return;

    setSelectedTimestamp(
      getElementAtEvent(chartRef.current, event)[0]["element"]["$context"][
        "parsed"
      ]["x"]
    );
  };

  const fileName = dayjs(selectedTimestamp).format("YYYY-MM-DD HH:mm:ss");
  const hasSelectedTimestamp = selectedTimestamp !== 0;

  return (
    <div className="App">
      <div className="Title">Rewind EEG</div>
      {!hasEEGData && (
        <ReactFileReader handleFiles={uploadFile} fileTypes={".csv"}>
          <div className="UploadBtn"> Upload EEG Data</div>
        </ReactFileReader>
      )}
      <div className="ChartArea">
        {hasEEGData ? (
          <Line
            ref={chartRef}
            data={chartData}
            options={options}
            onClick={onClick}
          />
        ) : (
          <></>
        )}
      </div>
      {hasSelectedTimestamp && (
        <div className="ScreenshotArea">
          <img
            className="ScreenshotImage"
            src={`/images/${fileName}.png`}
            alt="screenshot"
          />
          <div className="SummaryArea">
            This is the summary of your activity. You tend to get distracted
            when you have coding tasks.
          </div>
          {selectedTimestamp && <div>{fileName}</div>}
        </div>
      )}
    </div>
  );
}

export default App;
