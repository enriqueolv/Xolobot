
(cl:in-package :asdf)

(defsystem "arlo_nn_controller-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "AddTwoInts" :depends-on ("_package_AddTwoInts"))
    (:file "_package_AddTwoInts" :depends-on ("_package"))
    (:file "EvaluateDriver" :depends-on ("_package_EvaluateDriver"))
    (:file "_package_EvaluateDriver" :depends-on ("_package"))
  ))