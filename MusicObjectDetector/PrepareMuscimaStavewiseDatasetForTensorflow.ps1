$pathToGitRoot = "C:/Users/Alex/Repositories/MusicObjectDetector-TF"
$pathToSourceRoot = "$($pathToGitRoot)/MusicObjectDetector"
$pathToTranscript = "$($pathToSourceRoot)"

Start-Transcript -path "$($pathToTranscript)Transcript.txt" -append

cd $pathToSourceRoot
echo "Appending required paths to temporary PYTHONPATH"
$env:PYTHONPATH = "$($pathToGitRoot);$($pathToGitRoot)/research;$($pathToGitRoot)/research/slim;$($pathToSourceRoot)"

echo "Testing correct setup"
cd ../research
python object_detection/builders/model_builder_test.py

echo "Generating data-record in Tensorflow-format"
cd ../MusicObjectDetector

python download_muscima_dataset.py
python prepare_muscima_stavewise_annotations.py
python dataset_splitter.py --source_directory=data/muscima_pp_cropped_images_with_stafflines --destination_directory=data/training_validation_test

python create_muscima_tf_record.py --data_dir=data/training_validation_test --set=training --annotations_dir=Stavewise_Annotations --output_path=data/stave_crop_writer_independent_split/training.record --label_map_path=mapping_all_classes.txt
python create_muscima_tf_record.py --data_dir=data/training_validation_test --set=validation --annotations_dir=Stavewise_Annotations --output_path=data/stave_crop_writer_independent_split/validation.record --label_map_path=mapping_all_classes.txt
python create_muscima_tf_record.py --data_dir=data/training_validation_test --set=test --annotations_dir=Stavewise_Annotations --output_path=data/stave_crop_writer_independent_split/test.record --label_map_path=mapping_all_classes.txt

Stop-Transcript
