# Rewind EEG: Tracking Attention During Computer Tasks

Project for NeurotechX Global Hackathon 2023
https://neurotechx.com/hackathon2023/

Team members: Hayato Waki, Nao Yukawa, Toma Itagaki

Link to presentation: https://docs.google.com/presentation/d/1pRiOrAapx8Ue-Sz_HwQB4cc-JMDUUJs6CAuqoVmYJLI/edit?usp=sharing

Link to github: https://github.com/demind-inc/rewind-eeg

### Demo

![App Home Screen](/demo/app_home.png)

[Demo Video Link](https://drive.google.com/file/d/19OMNPED5wADM1fgzra7GScwKk630bISF/view?usp=sharing)

### Setup

#### Pre-requisite

You should have

- installed [Rewind.ai](https://www.rewind.ai/)
- measured your EEG with Emotiv

#### Set up database

First of all, export the video files from the local storage on your laptop via the command

```
python utils/rewind/convertRewindFilesToVideo
```

Thus, you will see videos exported under `utils/rewind/videos` folder.

#### Store your EEG data

Put your EEG data(CSV) under `data` folder.

### How to use

#### 1. Run the command to conduct the backend process

Run the command

```
python rewindEEG.py
```

in order to

- find the peak&trough points of attention from your EEG data
- take screenshots of your computar usage on those time points
- analyze them through GPT

#### 2. Run the frontend web app

```
cd front
npm run start
```

Run your web app.

### How it works

![Rewind](/demo/architecture.png)
