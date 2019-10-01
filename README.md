# Alexa Gadget Toolkit (AGT): Integration of Lego EV3 Brick with Amazon Echo
This tutorial can act as a continuation of an excellent [LEGO MINDSTORMS Voice Challenge](https://www.hackster.io/alexagadgets/lego-mindstorms-voice-challenge-setup-17300f) at Hackster.io. So, ideally you should complete all 4 missions from that challenge first and then jump to Step 1 of this tutorial to carry on.

If not, don't worry. Start with Step 0 below to setup the environment and then follow all other steps below in sequence.

## Pre-requisites: 
For this tutorial, you would need the following hardware components:
- Lego Mindstorms EV3 Robotics Kit. See the [Amazon link](https://www.amazon.co.uk/LEGO-31313-MINDSTORMS-Servo-Motor-Programmable/dp/B00BMKLVJ6);
- Amazon Echo device compatible with Alexa Gadget Toolkit. See the [Documentation link](https://developer.amazon.com/docs/alexa-gadgets-toolkit/understand-alexa-gadgets-toolkit.html#devices);
- Computer with the Internet connectivity and Visual Studio Code IDE. You can download Visual Studio Code from [here](https://code.visualstudio.com/download)
![ev3-and-echo](images/EV3_and_Echo_scene.jpg)

## Step 0 - Setup
1. Build your **EV3 robot**, following the instructions from the [Lego manual](https://www.lego.com/cdn/cs/set/assets/blt2fdb839be7a53b96/31313_EV3RSTORM_2016.pdf).
2. Next, install **ev3dev** (Debian Linux based operating system), so that you can launch Python 3.x based applications  on your EV3 Brick. Detailed installation instructions can be found [here](https://www.ev3dev.org/docs/getting-started/)
> **Note:** You need to complete steps 1 to 6 in **eve3dev** installation above. As a reward, in Step 6 EV3 robot will be able to read your fortune :-)
3. Then install **ev3dev-browser** extension as described in [Set up Visual Studio Code](https://www.hackster.io/alexagadgets/lego-mindstorms-voice-challenge-setup-17300f#toc-set-up-visual-studio-code-4).
4. Finally, [set up the Alexa Gadgets Toolkit (AGT) Python Software](https://www.hackster.io/alexagadgets/lego-mindstorms-voice-challenge-setup-17300f#toc-set-up-the-alexa-gadgets-toolkit-python-software-5), so that your EV3 robot can interact via **AGT interface** with your new Alexa skill that you will deploy shortly.

## Step 1 - Create your Alexa skill
1. Sign in with your Amazon developer account at [developer.amazon.com](https://developer.amazon.com/). If you don't have an account yet, you can create new one.
2. Then from the top menu select **Alexa -> Alexa Skills Kit**. ![screenshot_1.2](images/screenshot_step1.2.png)
3. Press **Create Skill** button and provide a name and default language for your new Alexa skill. ![screenshot_1.3](images/screenshot_step1.3.png)
4. In "Choose a model to add to your skill” section select **Custom**. ![screenshot_1.4](images/screenshot_step1.4.png)
5. In "Choose a method to host your skill's backend resources" section select **Alexa-Hosted (Node.js)**. ![screenshot_1.5](images/screenshot_step1.5.png)
6. Then press **Create skill** button in the upper right corner. It will take about one minute to create your skill and open it in Alexa Developer Console.
7. From the left navigation bar select **Interfaces**, then on the right side activate **Custom Interface Controller**. It will allow Echo device to send commands / directives to EV3 Brick and receive events from it back. ![screenshot_1.7](images/screenshot_step1.7.png)
8. Now from the left navigation bar select **JSON Editor**, then replace schema definition on the right with content from Git-attached **alexaskill-nodejs/model.json** file. ![screenshot_1.8](images/screenshot_step1.8.png)
9. Then **Save Model** and **Build Model** using buttons in the upper part of the screen. ![screenshot_1.9](images/screenshot_step1.9.png)
10. From the top navigation bar select **Code**, then copy content of Git-attached **alexaskill-nodejs/lambda/index.js, alexaskill-nodejs/lambda/package.json and alexaskill-nodejs/lambda/util.js** into relevant files under shown **Skill Code/lambda** directory. ![screenshot_1.10](images/screenshot_step1.10.png)
11. Click **create file** icon, enter the name as **lambda/common.js** and copy there content from Git-attached **alexaskill-nodejs/lambda/common.js**. ![screenshot_1.11](images/screenshot_step1.11.png)
12. **Save** all the changes, and the **Deploy** your Alexa skill, using relevant buttons in the upper part of the screen. ![screenshot_1.12](images/screenshot_step1.12.png)
13. Upon successful deployment, from the top navigation bar select **Test**, then enable testing in **Development**. ![screenshot_1.13](images/screenshot_step1.13.png)
14. Open your skill using Skill Invocation Name, e.g. "**open robot dice roller**". As you are using simulator, you should get a response, stating "**I couldn't find an EV3 Brick connected to this Echo device. Please check to make sure your EV3 Brick is connected, and try again.**". It proves that the new Alexa skill is functional, but cannot coonect to EV3 Brick yet - something that we'll look at in the next tutorial step. ![screenshot_1.14](images/screenshot_step1.14.png)
> **Note:** Invocation name can be set or changed in Alexa skill's **Build** section of Developer Console.

## Step 2 - Alexa Gadget registration
Your EV3 Brick needs to be registsred as an **Alexa Gadget** to enable its integration and data exchange with compatible Echo device. 
1. If you are still in Alexa Developer Console, click vertical ellipsis, select **Alexa Voice Service** option and then press **Products** button. ![screenshot_2.1](images/screenshot_step2.1.png)
2. Click **Create Product** button in the top right corner of the screen and fill in all the required fiedls. Ensure, that the product type is set to ***Alexa Gadget***, and the product category to ***Animatronic or Figure***. ![screenshot_2.2](images/screenshot_step2.2.png)

## Step 3 - Test EV3RSTORM with the Alexa skill

## High Level Overview of Solution Logic
```
pip install paho-mqtt
```

## Working model - Demo
You can find short demo of the working solution here on [YouTube](https://youtu.be/Gui9sqyglFw)

