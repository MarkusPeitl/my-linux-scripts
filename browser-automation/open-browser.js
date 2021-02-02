const puppeteer = require('puppeteer-core');
const fs = require('fs')
const { execSync } = require('child_process')
//fs.mkdirSync("./deafault")
//execSync("mkdir default")
//execSync("mkdir default")
(
    async () => {
        /*const browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium'
        });*/
        const browser = await puppeteer.launch(
            {
                //Navigate to chrome://version/ in chromium or chrome to get profile
                headless: false,

                //userDataDir: '/home/pmarkus/.config/google-chrome',
                //profileDirectory: 'Default',
                //executablePath: '/opt/google/chrome/google-chrome',

                userDataDir: '/home/pmarkus/snap/chromium/common/chromium',
                profileDirectory: 'Default',
                executablePath: 'chromium',
                noSandBox: true,
                autoClose: false
                //args: ['--no-sandbox'],
                

                //args: ['--user-data-dir=/home/pmarkus/.config/google-chrome/Default']


                //executablePath: '/snap/bin/chromium',
                //userDataDir: '~/snap/chromium/common/chromium/Default',
                //userDataDir: '/var/snap/chromium',
                //userDataDir: '~/.config/google-chrome',
                //executablePath: '/usr/bin/google-chrome',
                /*args: [
                    '--user-data-dir=~/snap/chromium/common/chromium',
                    '--profile-directory=Default',
                    '--no-sandbox'
                ],*/
            }
        );
        //const browser = await puppeteer.launch();
        //const page = await browser.newPage();
        //await page.goto('https://www.google.at/', {waitUntil: 'networkidle2'});
        //await page.goto('https://github.com');
        //await page.screenshot({path: 'example.png'});
        //await browser.close();
    }
)();