
# [this is ubuntu 20.04 for python3.7 (python3.7.13)]

links to the projects that are used
```
https://github.com/geohot/twitchslam
https://github.com/uoip/pangolin
https://github.com/uoip/g2opy
```
_____________________________________________________________________________________________________

## PANGOLIN

pangolin building instructions
```
git clone https://github.com/uoip/pangolin.git
cd pangolin
mkdir build
cd build
cmake ..
make -j8
cd ..
python setup.py install
```

If pangolin doesn't build check the requirements in g2opy section download them for pangolin and try it again (including making swap file)

```
conda install -c omnia eigen3 
conda install -c conda-forge suitesparse
conda install  glew

conda install -c conda-forge libglu             # (I am not so sure about this being necessary)
```

Not going to install c-compiler (I maybe used that for pangolin but it is not necessary it downgrades some gcc or g++ librarires from 9.4.0 to 9.3.0)

```
conda install -c conda-forge c-compiler 
```

```
conda install -c conda-forge doxygen
conda install -c conda-forge xorg-libxext
```

needed to download libdnet-dev

```
conda install -c anaconda mesa-libgl-cos6-x86_64
```

I run the below code at some point in the process 

```
conda update conda
conda env update
conda env update -f environment.yml (if you have the yml file for the environment with this you can download dependencies)
```

```
conda install -c psi4 gnu
conda install -c conda-forge coreutils
```

```
python 
>>> import pangolin  				(works I can import it)
```
WORKED						(it build pangolin.cpython-37m-x86_64-linux-gnu.so) (inside the pangolin directory)
_______________________________________________________________________________________________________________________

## G2OPY

g2opy building instructions
```
git clone https://github.com/uoip/g2opy.git			#(zip file exist no need this line)
cd g2opy							#(directory g2opy-master)
mkdir build
cd build
cmake ..
make -j8
cd ..
python setup.py install
```


conda environment for g2o alone (python specific)
```
conda create -n g2o_env python=3.7
```

dowloading dependencies from yml file
```
conda env update --file g2o_env2.yml 			#(-f for --file)
```

libraries that I downloaded for g2o

(and some of them also necessary for pangolin but I build them in separate environments and copied them to the twitchslam folder it worked?)

last three libraries are already being downloaded but if it doesn't you can use the codes

```
conda install -c anaconda cmake
conda install -c anaconda make

conda install -c omnia eigen3 

conda install -c conda-forge suitesparse

conda install -c conda-forge libglu 

conda install  glew
conda install -c conda-forge libglew-dev

conda install -c conda-forge pybind11
conda install -c conda-forge pybind11-global 

conda install -c conda-forge doxygen

conda install -c conda-forge libblas 
conda install -c conda-forge blas
conda install -c conda-forge liblapack
```

colab libraries
```
conda install -c eyeware eigen3 		(eigen3-3.3.4-0)	(search in conda website)
conda install -c nwani suitesparse 		(5.2.0)		(search in conda website)
```

files that are changed are below

eigen3                              omnia::eigen3-3.3.7-0 --> eyeware::eigen3-3.3.4-0

openssl            conda-forge::openssl-1.1.1q-h166bdaf_0 --> pkgs/main::openssl-1.1.1q-h7f8727e_0

suitesparse        conda-forge::suitesparse-5.10.1-h9e50~ --> nwani::suitesparse-5.2.0-h2ffa06c_0


```
conda run cmake --version    				# cmake version 3.22.1 (colab 3.22.6)
conda run make --version 				# GNU Make 4.2.1 (colab 4.1)
```

in colab

Setting up libsuitesparse-dev:amd64 (1:5.1.2-2) 

where is eigen info? (eigen version was close to eigen3-3.3.4-0)

ERROR
```
c++: fatal error: Killed signal terminated program cc1plus
compilation terminated.
```

SOLUTION 

solution to error was making 4GB swap file, check the link below (it worked also stopped freezing)
```
https://stdworkflow.com/1690/c-fatal-error-killed-signal-terminated-program-cc1plus
```
Adding swap file and activating
```
sudo mkdir -p /var/cache/swap/
sudo dd if=/dev/zero of=/var/cache/swap/swap0 bs=64M count=64
sudo chmod 0600 /var/cache/swap/swap0
sudo mkswap /var/cache/swap/swap0
sudo swapon /var/cache/swap/swap0
sudo swapon -s 			# (lists the running swap files)
```
Set the size of the partition bs=64M is the block size, count=64 is the number of blocks, so the swap space size is bs*count=4096MB=4GB


The path of the swap0 file is under /var/cache/swap/. After compiling, if you don't want the swap partition, you can delete it.
```
sudo swapoff /var/cache/swap/swap0
sudo rm /var/cache/swap/swap0
sudo swapoff -a 		# (Free space command)
```
After adding swap 
```
conda run cmake ..
conda run make
```
maybe I run codes below?
```
conda run cmake ..
make 					#(I remember that didn't work then I did it with "conda run make")
```              

I get the ERROR below

ERROR

```
make[2]: *** [python/CMakeFiles/g2o.dir/build.make:63：python/CMakeFiles/g2o.dir/g2o.cpp.o] error 1
make[1]: *** [CMakeFiles/Makefile2:1345：python/CMakeFiles/g2o.dir/all] error 2
make: *** [Makefile:130：all] error 2
```

SOLUTION

change the code below (before running cmake ..)
```
in g2opy/python/core/eigen_types.h line 185


        .def("x", (double (Eigen::Quaterniond::*) () const) &Eigen::Quaterniond::x)
        .def("y", (double (Eigen::Quaterniond::*) () const) &Eigen::Quaterniond::y)
        .def("z", (double (Eigen::Quaterniond::*) () const) &Eigen::Quaterniond::z)
        .def("w", (double (Eigen::Quaterniond::*) () const) &Eigen::Quaterniond::w)

to
        .def("x", [](const Eigen::Quaterniond& q) { return q.x(); })
        .def("y", [](const Eigen::Quaterniond& q) { return q.y(); })
        .def("z", [](const Eigen::Quaterniond& q) { return q.z(); })
        .def("w", [](const Eigen::Quaterniond& q) { return q.w(); })

```

WORKED 	(it build g2o.cpython-37m-x86_64-linux-gnu.so) (check the  /lib folder)
_____________________________________________________________________________________________________________________

## RUNNING ERRORS 
```
https://github.com/geohot/twitchslam
```

put "pangolin" and "g2o" ".so" files (names are something like down below) inside /twitchslam/lib/linux folder

g2o.cpython-37m-x86_64-linux-gnu.so

pangolin.cpython-37m-x86_64-linux-gnu.so


how to run twitchslam
```
export REVERSE=1   # Hack for reverse video
export F=500       # Focal length (in px)

./slam.py <video.mp4>

# good example
F=525 ./slam.py videos/test_freiburgxyz525.mp4

# ground truth
F=525 ./slam.py videos/test_freiburgrpy525.mp4 videos/test_freiburgrpy525.npz

# kitti example
REVERSE=1 F=984 ./slam.py videos/test_kitti984_reverse.mp4

# extract ground truth
tools/parse_ground_truth.py videos/groundtruth/freiburgrpy.txt videos/test_freiburgrpy525.npz 

```

didn't worked gave the ERROR below

ERROR
```
python slam.py videos/test_countryroad.mp4 
pygame 2.1.2 (SDL 2.0.16, Python 3.7.13)
Hello from the pygame community. https://www.pygame.org/contribute.html
using camera 1024x576 with F 280.000000

*** frame 0/781 ***
Traceback (most recent call last):
  File "slam.py", line 218, in <module>
    slam.process_frame(frame, None if gt_pose is None else np.linalg.inv(gt_pose[i]))
  File "slam.py", line 31, in process_frame
    frame = Frame(self.mapp, img, self.K, verts=verts)
  File "/home/ubuntu/Desktop/FOR-conda-and-others/SLAM/twitchslam-master/frame.py", line 74, in __init__
    self.kpus, self.des = extractFeatures(img)
  File "/home/ubuntu/Desktop/FOR-conda-and-others/SLAM/twitchslam-master/frame.py", line 17, in extractFeatures
    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
  File "/home/ubuntu/Desktop/FOR-conda-and-others/SLAM/twitchslam-master/frame.py", line 17, in <listcomp>
    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
cv2.error: OpenCV(4.6.0) :-1: error: (-5:Bad argument) in function 'KeyPoint'
> Overload resolution failed:
>  - KeyPoint() missing required argument 'size' (pos 3)
```

SOLUTION
```
change the code

in frame.py line 17

 kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]    #it was _size make it size 
 kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], size=20) for f in pts]
```



__________________________________________________________________________
__________________________________________________________________________

### SOME NOTES ALONG THE JOURNEY
__________________________________________________________________________
__________________________________________________________________________
### ERRORS  while building G2OPY


causes ERROR DO NOT DOWNLOAD IT (if you download it)

#do not install libc gives [Segmentation fault (core dumped) ERROR] (after couple of ctrl+C it also gaves the same ERROR it also happens when computer runs out of memory) and  uninstalling Miniconda and installing it again doesn't solve the problem, delete  libc in yml files

```
conda install -c groakat libc
conda remove -c groakat libc
```

I download it before, no need to download that   (while building I think that is not the problem) (and python cannot import that)

```
conda install -c conda-forge g2o
conda remove -c conda-forge g2o
```

I am going to do

```
conda clean -a    	#that will delete some things ? (doesn't solve libc core dump)

conda update conda

conda install --f environment.yml
```
or
```
conda env create -f environment.yml 
```


ERROR
```
fatal error: Python.h: No such file or directory
```
SOLUTION
```
sudo apt-get install python3-dev
sudo apt install libpython3.7-dev
```

if still persists
```
sudo apt-get install python-dev   			# (for python2.x installs)
```



__________________________________________________________________

### INFO




(download everything with "conda install" if they have the sources. Go in their website and search it)

(without using "conda environments" it uses "conda base", but without "conda run cmake .. "and without "conda run make" it runs inside the terminal without being isolated)


base is also a conda environment but I didn't dowload all the necessary parts there 

```
conda install -c omnia eigen3 
```

CHOLMOD not found error being solved
```
sudo apt-get install -y libsuitesparse-dev
```
I used below code for solving the CHOLMOD problem in conda
``` 
conda install -c conda-forge suitesparse
```

for exporting environment info 		(like pip freeze > requirements.txt)
```
conda env export > environment.yml
```
creating environment from a yml file
```
conda env create -f environment.yml 
```

deactivating the environment
```
conda deactivate
```
deleting the environment
```
conda env remove -n for_slam 
```

what was that for, I cannot quite remember
```
conda env create -f environment.yml 
conda update -n base -c defaults conda
```

Deleting the Miniconda
```
rm -rf ~/miniconda3 		#becareful with M,m 3 or not
```


for making "cmake" and "make" run in conda 			(for_slam environment)

```
conda run cmake ..
conda run make 					(doesn't show output but it works)
```

I run "conda run cmake .." then "make" without "conda" couple of times



_______________________________________________________________________

### NOT NECESSARY FORG G2OPY

that was NOT NECESSARY for g2o

```
conda install -c anaconda hdf5 
```

didn't solve (Could NOT find QGLVIEWER (missing: QGLVIEWER_INCLUDE_DIR)) 
```
conda install -c conda-forge libqglviewer
```


DO NOT DOWNLOAD this
```
conda install -c conda-forge c-compiler 
```

if necessary to download python3.7 again
```
conda install python==3.7.13
```

try with new environment DO NOT DOWNLOAD  these

```
conda install -c conda-forge glib
conda install -c anaconda mesa-libgl-cos6-x86_64
```

core dumping ERROR DO NOT DOWNLOAD  these
```
conda install -c groakat libc
conda remove -c groakat libc

conda install -c rmg glibc
conda remove -c rmg glibc
```
didn't use the codes below yet  			(maybe it will be helpful with some errors)
```
wget http://mirrors.kernel.org/ubuntu/pool/main/g/glibc/libc6_2.23-0ubuntu10_amd64.deb
wget http://mirrors.kernel.org/ubuntu/pool/main/g/glibc/libc6-dev_2.23-0ubuntu10_amd64.deb

$ # Unpack files into current directory (will create usr/ and lib/ and lib64/ folders)
$ ar p libc6_2.23-0ubuntu10_amd64.deb data.tar.xz | tar xvJ
$ ar p libc6-dev_2.23-0ubuntu10_amd64.deb data.tar.xz | tar xvJ
```



if necessary, instead of libc try this. I didn't use that yet 
```
conda install libgcc
```
________________________________________________________________



### FOR GENERAL

Just because I am doing "make" without "conda", "eigen" is not exist codes below are for downloading it

For computer itself not for "conda environments" also not for "conda base"

```

sudo apt-get install libglew-dev			# (conda install glew) (is enough for conda environments)
sudo apt-get install libeigen3-dev      		# (both for pangolin and g2o I guess?)
sudo apt-get install -y libsuitesparse-dev
```
______________________________________________________________

### WHILE RUNNING TWITCHSLAM

Inspection of python3.6 packages for python3.7 (if there is an error regarding to the versions of the libraries)

```
sudo add-apt-repository -y ppa:jblgf0/python
sudo apt-get update
sudo apt-get install python3.6
```

Then build virtualenv for python3.6 and download packages (just names not spesific version)
```
virtualenv py36-env --python=python3.6
source py36-env/bin/activate
```
```
pip install -r twitcslam_requirements_names.txt
sudo apt-get install python3.6-distutils
```
Didn't solved the ERROR



Meanwhile activate for_slam conda environment
```
conda create -n for_slam python=3.7
conda env update --file for_slam.yml 
```
Then download twitchslam requirements

```
pip install -r SLAM-env-requirements.txt
slam.py video/test_c..mp4
```
Didn't worked same ERROR occured

________________________________________________________________________________________________

### CONDA-STUFF (some of that code is being used while building pangolin if got an ERROR come here and check if something missing)
```
https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
```

Download

Python 3.7 	Miniconda3 Linux 64-bit

```
sudo chmod +x Miniconda3-py37_4.12.0-Linux-x86_64.sh
bash Miniconda3-py37_4.12.0-Linux-x86_64.sh
conda update conda
```
```
conda -V   --->  conda 4.13.0
```
Creating virtual environment
```
conda create -n yourenvname python=x.x anaconda
source activate yourenvname
```

```
conda install git
conda config --append channels conda-forge    #(not necessary you can download without adding a channel just search in conda website)
```
Didn't worked 

```
conda install -c conda-forge libglew-dev
```
I find this

```
https://anaconda.org/conda-forge/glew
```
```
conda install  glew
```
That's not a code just what I saw on the terminal
```
The following NEW packages will be INSTALLED:

  glew               pkgs/main/linux-64::glew-2.1.0-h295c915_3
  libglu             pkgs/main/linux-64::libglu-9.0.0-hf484d3e_1
```

google search   "conda eigen"
```
 conda install  eigen
```
```
https://anaconda.org/conda-forge/eigen
```
```

The following NEW packages will be INSTALLED:

  eigen              pkgs/main/linux-64::eigen-3.3.7-hd09550d_1
```
```
https://anaconda.org/omnia/eigen3
```
```
conda install -c omnia eigen3 
```
```
conda list   		# (shows downloaded packages)
conda install -c anaconda cmake
conda run cmake ..        
conda install -c conda-forge gcc   			# (downgrading so I said no)
conda install -c conda-forge suitesparse 		# (for CHOLMOD error)
conda install -c anaconda make
conda run make 
conda install -c conda-forge pybind11
```

```
conda install -n yourenvname [package]
conda activate yourenvname
source deactivate 	(or conda deactivate)
conda remove -n yourenvname -all

```
shows what is in the environment (like pip freeze)
```
conda env create -f environment.yml
```

also for uninstalling check the link below
```
https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
```

environment location: /home/ubuntu/miniconda3/envs/for_slam

pkgs/main/linux-64::_libgcc_mutex-0.1-main

pkgs/main/linux-64::gettext-0.21.0-hf68c758_0

Read

```
https://www.activestate.com/resources/quick-reads/how-to-manage-python-dependencies-with-conda/
```
