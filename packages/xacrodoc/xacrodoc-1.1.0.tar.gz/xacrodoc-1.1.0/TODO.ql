~ optionally resolve package:// directives automatically (this a URDF thing not
  xacro)
  - add a test for this
~ update dependencies
~ remove ROS checks from tests
~ move xacrodoc into its own file and import the finder in `__init__.py`
~ consider if there is a better way to install the required ROS toolchain to
  enable on systems without ROS
  - the ros2 branch of xacro is more self-contained
  - need some more general way of resolving packages (see below)
  - probably want to make this separately installable but I need my own fork
~ possibly remove ROS package stuff
  - need a package.xml to mark this as a package
~ xacro issue to resolve the change in find/arg behaviour
~ consider adding a `pkgpaths` variable in PackageFinder to directly specify a
  dictionary of package paths
  - more generally, may want to cache results of directory look-ups, similar to
    (how I think) rospack works

* make finder local to each package: this would require somehow resolving
  $(find ...) directives myself (so that _eval_find need never be called), but
  this seems difficult
