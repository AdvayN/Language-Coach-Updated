import streamlit as st

from Utils import save_audio_wav
import gladia_utils as gut
import references as ref
import evaluation_utils as eu

REFERENCE_MAPPER = {
    "SWO": ref.SWO,
    "BLO": ref.BLO,
    "BOOK": None
}


# add the title and emojis
st.title("🎯 Pronunciation Test")

# upload an audio file
uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'ogg'])

# column for selecting test level and test type
col_one, col_two = st.columns(2)

with col_one:
    test_level = st.selectbox("Select Test Level", ["Level 5"])

with col_two:
    test_type = st.selectbox("Select Test Type", ["SWO", "BLO", "BOOK"])

# decide the reference type
reference = REFERENCE_MAPPER.get(test_type, None)
if not reference:
    st.error("Invalid reference type selected!", icon = "🚨")
    st.stop()

if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Define output file path
    output_path = "converted_file.wav"

    # Save uploaded file as .wav
    save_audio_wav(uploaded_file.read(), output_path)
    # start processing the audio for pronounciation
    with st.spinner("Testing Pronounciation....."):
        # add a toast for processing
        st.toast("Processing Audio for Pronounciation", icon = "🚀")
        # upload the file to gladia
        audio_upload_response = gut.upload_file_to_gladia(output_path)
        audio_url = audio_upload_response["audio_url"]
        if not audio_url:
            # error with an emoji
            st.error("Audio upload failed. Please try again!", icon = "🚨")
            st.stop()
        # initiate the transcribe job
        audio_id_response = gut.transcribe_audio(audio_url)
        audio_id = audio_id_response["transcription_id"]
        if not audio_id:
            # error with an emoji
            st.error("Audio transcription failed. Please try again!", icon = "🚨")
            st.stop()
        # get the transcription
        transcript_response = gut.poll_transcription(audio_id)
        audio_transcript = transcript_response.get("transcript", None)
        audio_status = transcript_response.get("status", None)
        if not audio_transcript:
            # error with an emoji
            st.error(f"Audio transcription failed. Please try again! Audio status: {audio_status}", icon = "🚨")
            st.stop()
        # do the evaluation
        evaluation = eu.evaluate_pronounciations(audio_transcript, reference)
        # add a toast for evaluation completed
        st.toast("Evaluating Pronounciation Completed", icon = "🚀")
        # display the evaluation more attractively
        # header with emoji
        st.subheader("🎯 Evaluation Results")
        st.dataframe(evaluation, width="stretch")
    st.success("Evaluation Completed")
    # download button to download the evaluation csv
    st.download_button(
        label="Download Evaluation CSV",
        data=evaluation.to_csv(index=False),
        file_name="evaluation.csv",
        mime="text/csv",
        on_click="ignore"
    )