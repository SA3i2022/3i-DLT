function[filename]=get_npy_file(path, cap_number,channel)

prac=dir(path)
for i = 1:length(prac)
    if contains(prac(i).name,cap_number) && contains(prac(i).name,'.imgdir')
        a=prac(i).name;
        break;
    end
end
np=fullfile(path, a)
new_path = dir(np);
for z = 1:length(new_path)
    if contains(new_path(z).name,channel) && contains(new_path(z).name, 'ImageData')
        c=new_path(z).name;
        break;
    end
end
filename=fullfile(np,c)
   



