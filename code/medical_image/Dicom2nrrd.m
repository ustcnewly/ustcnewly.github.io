function [] = Dicom2nrrd(dicomPath)
%{
Function which reads a DICOM image and save it as NNRD image.

INPUT:
        dicomPath: the path of the DICOM image to be processed.
        path_out: the path where to save the two output files. Without file
        extension.

OUTPUT:
        None, the function itself saves the output file. 

NOTE: Information about NRRD header in: http://teem.sourceforge.net/nrrd/format.html

PROJECT: PIM - MUI-TIC

DATE: 22/03/2015

VERSION: 1?

AUTHOR: Jesús Monge Álvarez
%}
% clc; clear all; close all;
%% Checking the input parameters of the function:
control = ~isempty(dicomPath);
assert(control,'You must indicate the directory of a DICOM image.');
% We extract the information of the input DICOM file:
[~,name,dicomExt] = fileparts(dicomPath);
format = dicomExt(2:end); % We eliminate the '.' of the extension
format = lower(format);
control = ((~strcmp(format,'dc3')) && (~strcmp(format,'dcm')) && (~strcmp(format,'dic')) ...
        && (~strcmp(format,'dicom')) && (~isempty(format)));
assert(~control,'The type of input file is not supported. Only DICOM files');


%% Reading the raw data in the the DICOM file:
%dicomPath = 'D:\MUI-TIC\Procesado_imagen_medica\Datos_clinicos\EPA_13\DICOM\IM_0001';
I = dicomread(dicomPath); I = squeeze(I);

%% Composing the header of the NRRD file:
disp('Composing the NRRD header...');
% We get the kind of data we will store:
dicomClass = class(I);
switch (dicomClass)
    case {'int8','uint8','int16','uint16','int32','uint32','int64','uint64','double'}
        nrrdType = dicomClass;
    case 'single'
        nrrdType = 'float';
    otherwise
        assert(false,'The data type of the DICOM file is unknown.')
end
% We get the size of the data:
nrrdDims = size(I);
nrrdNumDims = length(nrrdDims);
% We compose the rest of the header according to the number of dimensions in the raw data:
switch nrrdNumDims
    case 2
        nrrdSpace = 'left-posterior';
        nrrdOrigin = '(0,0)';
        nrrdSpaceDirections = '(1,0) (0,1)';
        nrrdCenterings = 'cell cell';
        nrrdKinds = 'space space';
    case 3
        nrrdSpace = 'left-posterior-superior';
        nrrdOrigin = '(0,0,0)';
        nrrdSpaceDirections = '(1,0,0) (0,1,0) (0,0,1)';
        nrrdCenterings = 'cell cell cell cell';
        nrrdKinds = 'space space space';
    case 4
        nrrdSpace = 'left-posterior-superior-time';
        nrrdOrigin = '(0,0,0,0)';
        nrrdSpaceDirections = '(1,0,0,0) (0,1,0,0) (0,0,1,0) (0,0,0,1)';
        nrrdCenterings = 'cell cell cell cell';
        nrrdKinds = 'space space space time';   
end
nrrdSizes = num2str(nrrdDims);
nrrdDimensions = num2str(nrrdNumDims);
nrrdModality = '=Scalar';
nrrdEncoding = 'raw';
nrrdEndian = 'little';
fprintf('\tNRRD header successfully composed.\n');

%% Writing the NRRD file:
% We create a new '.nrrd' file:
disp('Creating ''.nrrd'' file...');
nrrdID = fopen(strcat(name,'.nrrd'),'w+'); % Open or create file for reading and wrinting
if nrrdID ~= -1
    fprintf('\tNew ''.nrrd'' file successfully created.\n');
end
% We write the NRRD header:
disp('Writing the NRRD header...');
fprintf(nrrdID,'NRRD0004\n'); % NRRD of 4th version
fprintf(nrrdID,['type: ',nrrdType,'\n']);
fprintf(nrrdID,['dimension: ',nrrdDimensions,'\n']);
fprintf(nrrdID,['space: ',nrrdSpace,'\n']);
fprintf(nrrdID,['sizes: ',nrrdSizes,'\n']);
fprintf(nrrdID,['spacedirections: ',nrrdSpaceDirections,'\n']);
fprintf(nrrdID,['centerings: ',nrrdCenterings,'\n']);
fprintf(nrrdID,['kinds: ',nrrdKinds,'\n']);
fprintf(nrrdID,['endian: ',nrrdEndian,'\n']);
fprintf(nrrdID,['encoding: ',nrrdEncoding,'\n']);
fprintf(nrrdID,['spaceorigin: ',nrrdOrigin,'\n']);
control = fprintf(nrrdID,['modality:',nrrdModality,'\n']);
if control ~= 0
    fprintf('\tNRRD header successfully writed.\n');
end
% We write the raw data in the NRRD file:
fprintf(nrrdID,'\n');
disp('Writing the raw data in the NRRD file...');
control = fwrite(nrrdID,I,nrrdType);
if control ~= 0
    fprintf('\tRaw data successfully writed in the NRRD file.\n');
end

%% Closing the NRRD file:
control = fclose(nrrdID);
disp('Closing the NRRD file...');
if control == 0
    fprintf('\tNRRD file successfully closed.\n');
end

end % End of the function 'mydicom2nrrd'
