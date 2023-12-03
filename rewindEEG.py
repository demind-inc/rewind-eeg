from utils.rewind.videoAnalylze import analyze_video
from utils.analysis import handleEEG
from utils.gpt import summarizeScreenshots
import utils.gpt.config as config
from openai import OpenAI

def generate_summary(peak_summaries, trough_summaries):
    client = OpenAI(
        api_key=config.api_key
    )
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"A user has high attention during {peak_summaries} and low attention during {trough_summaries}. Can you generate an actionable guide for how the user can maximize their productivity."}
        ]
    )
    response = completion.choices[0].message.content
    return response

if __name__ == "__main__":
    datafile = 'data/Emotiv-one-hour.csv'
    peak_points, trough_points = handleEEG.find_attention_points(datafile)

    peak_summary = []
    for pp in peak_points['Timestamp']:
        ppts = handleEEG.convert_timestamp_to_nyt(pp)
        filename = analyze_video(ppts)
        print(filename)
        summary = summarizeScreenshots.summarizeScreenshot('utils/rewind/screenShots/' + filename +'.png')
        task_summary = summarizeScreenshots.validateJSON(summary)
        print(summary)
        if task_summary:
            peak_summary.append(task_summary)
        else:
            peak_summary.append('no task')
    print(peak_summary)

    trough_summary = []
    for tp in trough_points['Timestamp']:
        tpts = handleEEG.convert_timestamp_to_nyt(tp)
        filename = analyze_video(tpts)
        print(filename)
        summary = summarizeScreenshots.summarizeScreenshot('utils/rewind/screenShots/' + filename +'.png')
        task_summary = summarizeScreenshots.validateJSON(summary)
        print(summary)
        if task_summary:
            trough_summary.append(task_summary)
        else:
            trough_summary.append('no task')
    print(trough_summary)
    output = generate_summary(peak_summary, trough_summary)

    # a = ['software development', 'email communication', 'slack response', 'youtube', 'software development']
    # b = ['zoom meeting', 'zoom meeting', 'writing paper', 'reading articles', 'citations']
    # output = generate_summary(a, b)
    
    # output gpt summary to an output.txt
    with open('output.txt', 'w') as file:
        file.write(output)
    print(output)



    