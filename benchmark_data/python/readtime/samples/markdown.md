Want to add a feature or automate something in your [NetBeans IDE](https://netbeans.org/)? Follow along as we write your first plugin for NetBeans.

Let's go beyond the simple [Toolbar Example](https://platform.netbeans.org/tutorials/nbm-google.html) and create a plugin which can auto-update itself.
This code is based on the [WakaTime plugin for NetBeans](https://github.com/wakatime/netbeans-wakatime). Our example plugin will simply print a Hello World statement and update to new versions if available... just enough to get you started.

## Create a new Plugin Project

Choose `File` -> `New Project` then `NetBeans Modules` -> `Module` as the project type.

![Create Plugin Project](https://wakatime.com/static/img/blog/create-plugin-project.png)


Name your project

![Name Your Project](https://wakatime.com/static/img/blog/name-your-project.png)


Choose a namespace or code name for your plugin

![Namespace Your Project](https://wakatime.com/static/img/blog/namespace-your-project.png)


## Add a Java File

![Create Java File](https://wakatime.com/static/img/blog/create-java-file.png)

![Name Java File](https://wakatime.com/static/img/blog/name-java-file.png)


## Plugin Starting Point

After creating the new Java Class file, make it extend [ModuleInstall](http://bits.netbeans.org/7.4/javadoc/org-openide-modules/org/openide/modules/ModuleInstall.html) and wrap it with [@OnShowing](http://bits.netbeans.org/dev/javadoc/org-openide-windows/org/openide/windows/OnShowing.html) so it only runs after the GUI has loaded.

```java
@OnShowing
public class MyPlugin extends ModuleInstall implements Runnable {
}
```

Press <kbd>ALT</kbd> + <kbd>ENTER</kbd> with your cursor over `OnShowing` then select `Search Module Dependency for OnShowing` to import the Window System API into the project. This will add a new dependency to your project as well as add the necessary import statements to the top of your file. Also do this for `ModuleInstall`.

![Search Module Dependency](https://wakatime.com/static/img/blog/search-module-dependency.png)

Sometimes NetBeans misses the `org.openide.util` dependency, so you might have to add that one manually. To do that, right click on <keyword>MyPlugin</keyword> then select `Properties`.

![Project Properties](https://wakatime.com/static/img/blog/project-properties.png)

Choose category `Libraries` then click `Add...`. Type `org.openide.util` then click `OK`. This will add the dependency to your `project.xml` file.

![Project Properties Libraries](https://wakatime.com/static/img/blog/project-properties-libraries.png)

![Add Utilities API](https://wakatime.com/static/img/blog/add-utilities-api.png)

Press <kbd>ALT</kbd> + <kbd>ENTER</kbd> on your <keyword>MyPlugin</keyword> class, then choose `Implement all abstract methods`.

![Implement Abstract Methods](https://wakatime.com/static/img/blog/implement-abstract-methods.png)

One last thing, add this line to your `manifest.mf` file.

`OpenIDE-Module-Install: org/myorg/myplugin/MyPlugin.class`

![OpenIDE Module Install](https://wakatime.com/static/img/blog/openide-module-install.png)

Now the `run()` method will execute after your plugin has loaded.

![First Time Running](https://wakatime.com/static/img/blog/plugin-has-loaded.png)


## Logging

Let's make that `println` output to the NetBeans IDE log. First, setup the logger as an attribute of your <keyword>MyPlugin</keyword> class.

```java
public static final Logger log = Logger.getLogger("MyPlugin");
```

Press <kbd>ALT</kbd> + <kbd>ENTER</kbd> to import [java.util.logging.Logger](https://encrypted.google.com/search?q=java.util.logging.Logger+site%3Ahttps%3A%2F%2Fdocs.oracle.com).

![Add Logger Import](https://wakatime.com/static/img/blog/add-logger-import.png)

Replace `println` with `log.info("MyPlugin has loaded.");`.

![Log Line](https://wakatime.com/static/img/blog/log-line.png)


## Updating Your Plugin Automatically

Create a new Java file `UpdateHandler.java` inside your <keyword>MyPlugin</keyword> package.

Replace the contents of this file with [UpdateHandler.java](https://gist.github.com/alanhamlett/2a57ffb51f0850272d0d). Search the module dependency and add any missing dependencies by pressing <kbd>ALT</kbd> + <kbd>ENTER</kbd> over each import statement.

Add these lines to your `manifest.mf` file.

```java
OpenIDE-Module-Layer: org/myorg/myplugin/layer.xml
OpenIDE-Module-Implementation-Version: 201501010101
```

Create a new XML document in your <keyword>MyPlugin</keyword> package.

![New XML Document](https://wakatime.com/static/img/blog/new-xml-document.png)

![Name XML Document](https://wakatime.com/static/img/blog/name-xml-document.png)

```java
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE filesystem PUBLIC "-//NetBeans//DTD Filesystem 1.2//EN" "http://www.netbeans.org/dtds/filesystem-1_2.dtd">
<filesystem>
    <folder name="Services">
        <folder name="AutoupdateType">
            <file name="org_myorg_myplugin_update_center.instance">
                <attr name="displayName" bundlevalue="org.myorg.myplugin.Bundle#Services/AutoupdateType/org_myorg_myplugin_update_center.instance"/>
                <attr name="enabled" boolvalue="true"/>
                <attr name="instanceCreate" methodvalue="org.netbeans.modules.autoupdate.updateprovider.AutoupdateCatalogFactory.createUpdateProvider"/>
                <attr name="instanceOf" stringvalue="org.netbeans.spi.autoupdate.UpdateProvider"/>
                <attr name="url" bundlevalue="org.myorg.myplugin.Bundle#org_myorg_myplugin_update_center"/>
            </file>
        </folder>
    </folder>
</filesystem>
```

Add this code to your <keyword>MyPlugin</keyword> class inside the `run()` method.

```java
WindowManager.getDefault().invokeWhenUIReady(new Runnable () {
    @Override
    public void run() {
      UpdateHandler.checkAndHandleUpdates();
    }
});
```

Add these lines to your `Bundle.properties` file:

```java
Services/AutoupdateType/org_myorg_myplugin_update_center.instance=MyPlugin
UpdateHandler.NewModules=false
org_myorg_myplugin_update_center=https\://example.com/updates.xml
```

Now every time NetBeans restarts and launches your plugin, it will check for updates by downloading `updates.xml` from example.com.

Your updates.xml file tells NetBeans where to get the new NBM of your plugin.
To create an NBM for publishing your plugin, right click on your <keyword>MyPlugin</keyword> project and select `Create NBM`. The NBM file is what you will publish to the [NetBeans Plugin Portal](http://plugins.netbeans.org/).

For an example of hosting `updates.xml` on GitHub, look at [update.xml](https://github.com/wakatime/netbeans-wakatime/blob/master/updates.xml) and corrosponding [Bundle.properties](https://github.com/wakatime/netbeans-wakatime/blob/master/src/org/wakatime/netbeans/plugin/Bundle.properties) from the [WakaTime NetBeans plugin](https://github.com/wakatime/netbeans-wakatime/).
