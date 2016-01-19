FROM python:3.5

MAINTAINER Alessandro Molari <molari.alessandro@gmail.com> (alem0lars)

ENV PORT 3000
ENV LEVELS_PWDS /tmp/levels-passwords

# ☞ Prepare storage for NLaunch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# ☞ Build & Install NLaunch ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COPY . /usr/src/app
RUN pip install --no-cache-dir -r console/requirements.txt

CMD [ "python3.5", "./console/main.py" ]
