from rest_framework import serializers

from api.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['processed']

    def is_valid(self, *, raise_exception=False):
        # Default validating
        super().is_valid(raise_exception=raise_exception)

        # Getting file extension
        file_name = self.validated_data['file'].name
        file_name_split = file_name.split('.')
        file_ext = ''
        if len(file_name_split) > 1:
            file_ext = file_name_split[-1]

        # Checking file extension
        file_type = self.validated_data.get('type')
        if (file_type and file_type != File.FileTypeChoices.NA and
            file_ext.lower() not in File.VALID_FILES_EXTENSIONS[file_type]):

            valid_file_exts_str =\
                ', '.join(File.VALID_FILES_EXTENSIONS[file_type])
            error_msg = (f'File extension {file_ext} is not valid'
                         f' for file type {file_type}.'
                         f' Valid file extensions for this file type:'
                         f' {valid_file_exts_str}.')
            if not self.errors.get('type'):
                self._errors['type'] = []
            self._errors['type'].append(error_msg)

            if raise_exception:
                raise serializers.ValidationError(self.errors)

        return not bool(self._errors)