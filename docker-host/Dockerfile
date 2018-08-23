FROM Alpine:3.8

RUN ["mkdir", "/home/ansible"]

WORKDIR /home/ansible

RUN ["apk", "update"]
RUN ["apk", "add", "python"]
RUN ["apk", "add", "ansible"]
RUN ["apk", "add", "git"]

RUN ["git", "clone", "https://github.com/alair-aurea/ansible-scripts.git"]

RUN ["mkdir", "downloads"]
RUN ["cd", "downloads"]
RUN ["wget", "https://www.yourkit.com/download/YourKit-JavaProfiler-2018.04-b81.zip"]
RUN ["unzip", "YourKit-JavaProfiler-2018.04-b81.zip"]
RUN ["mv", "YourKit-JavaProfiler-2018.04", "/home/ansible/ansible-scripts/files/YourKit-linux"]

RUN ["cd", "/home/ansible"]



