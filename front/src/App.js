import React, { useState, useRef, useEffect } from "react";
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

  const fileName = dayjs(selectedTimestamp).format("YYYY-MM-DD HH:mm:ss");

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
          {selectedTimestamp && <div className="Timestamp">{fileName}</div>}
          <div className="SummaryArea">
            <b>1. Capitalize on Peak Times:</b> The user should understand when
            their attention span is at its peak, usually in the mornings after a
            refreshing sleep, to work on tasks that require maximum
            concentration. Schedule software development tasks during these
            times, since they seem to have the highest attention levels during
            these activities.
            <br />
            <b>2. Communicate Via Emails and Slack:</b> It seems the user does
            an excellent job responding to emails and slack messages. They
            should continue utilizing these platforms for the primary
            communication since it helps them stay focused and organized.
            <br />
            <b>3. Limit Usage of YouTube: </b>While the user seems to have high
            attention towards YouTube, it’s tons of diverse content might
            deviate them from their objective. Use YouTube only for constructive
            purposes, like tutorials related to software development, learning
            new skills, or getting assistance in ongoing tasks.
            <br />
            <b> 4. Optimizing Zoom Meetings:</b> The user seems to lose focus
            during Zoom meetings, therefore find ways to make these meetings
            more engaging. Make use of visual aids, have interactive sessions,
            and ensure the agenda is clear from the beginning. If possible, see
            if some meetings can be handled via email or slack messages instead.
            <br />
            <b>5. Strategic Approach Towards Reading and Writing</b> The user
            appears to have low attention while reading articles, writing paper,
            and citing. They can try different strategies such as the Pomodoro
            technique, where they work for a fixed duration (25 minutes) with no
            distractions, followed by a 5-minute break. Gradually, they can
            increase the work time to an hour and then take a longer break. For
            reading articles, they can use tools that highlight the main points
            of the article. While writing or citing, keeping a clear structure
            and frequent breaks can help maintain interest.
            <br />
            <b>6. Physical Exercise and Rest:</b> It's essential to maintain a
            balance between work and relaxation. Adequate sleep and regular
            physical exercise can significantly improve one's focus and
            concentration.
            <br />
            <b>7. Use of Productivity Tools:</b> Utilize productivity tools and
            applications. They can help manage time better, keep track of tasks,
            set goals and reminders, and ultimately help the user focus better.
            <br />
            <b>8. Healthy Eating:</b> Eating a well-balanced diet can have a
            significant impact on attention and productivity levels. Avoid too
            much caffeine or energy drinks which can cause energy crashes.
            Instead, opt for brain-boosting foods like fruits, nuts, and enough
            water.
            <br />
            <b>9. Mental Health:</b> Take care of mental health by practicing
            mindfulness or relaxation exercises. Stress and anxiety can play
            significant roles in affecting attention levels.
            <br />
            <b>10. Setting Priorities:</b> For every day or week, have a clear
            set of goals and tasks to be accomplished. This keeps the user
            focused and prevents them from diverting to less important tasks.
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
