import streamlit as st

from Utils import save_audio_wav
import gladia_utils as gut
import references as ref
import evaluation_utils as eu
option = st.selectbox("Select An Option", ["Upload a txt file","Choose a file"])
if option == "Upload a txt file":
    reftxtfile = st.file_uploader("Choose a reference text file", type=['txt'])
    if reftxtfile is not None:
     # Read file as text
        text = reftxtfile.read().decode("utf-8")
        reference = f'"""\n{text}\n"""'
    else:
        st.warning("Please Upload a txt file")
        st.stop()
elif option== "Choose a file":
    # column for selecting test level and test type
    col_one, col_two = st.columns(2)

    with col_one:
        test_level = st.selectbox("Select Test Level", ["Level 5"])

    with col_two:
        test_type = st.selectbox("Select Test Type", ["SWO", "BLO", "BOOK"])

    # decide the reference type
    if test_level=="Level 5":
        reference = ref.Level_5[test_type]
    else:
        None
    # if not reference:
    #     st.error("Invalid reference type selected!", icon = "🚨")
    #     st.stop()
    
# REFERENCE_MAPPER = {
#     "SWO": ref.SWO,
#     "BLO": ref.BLO,
#     "BOOK": None
# }

# REFERENCE_MAPPER = {
#     "SWO": wrapped_text,
#     "BLO": ref.Level_5["BLO"],
#     "BOOK": None
# }

# add the title and emojis
st.title("🎯 Pronunciation Test")
audio_option = st.selectbox("Select An Option", ["Upload an audio file","Record Audio"])
if audio_option == "Upload an audio file":
    # upload an audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'ogg'])
elif audio_option == "Record Audio":
    uploaded_file = st.audio_input("Record your audio")

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
        st.success(audio_transcript)
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