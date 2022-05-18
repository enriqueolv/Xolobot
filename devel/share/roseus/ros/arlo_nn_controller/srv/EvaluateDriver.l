;; Auto-generated. Do not edit!


(when (boundp 'arlo_nn_controller::EvaluateDriver)
  (if (not (find-package "ARLO_NN_CONTROLLER"))
    (make-package "ARLO_NN_CONTROLLER"))
  (shadow 'EvaluateDriver (find-package "ARLO_NN_CONTROLLER")))
(unless (find-package "ARLO_NN_CONTROLLER::EVALUATEDRIVER")
  (make-package "ARLO_NN_CONTROLLER::EVALUATEDRIVER"))
(unless (find-package "ARLO_NN_CONTROLLER::EVALUATEDRIVERREQUEST")
  (make-package "ARLO_NN_CONTROLLER::EVALUATEDRIVERREQUEST"))
(unless (find-package "ARLO_NN_CONTROLLER::EVALUATEDRIVERRESPONSE")
  (make-package "ARLO_NN_CONTROLLER::EVALUATEDRIVERRESPONSE"))

(in-package "ROS")





(defclass arlo_nn_controller::EvaluateDriverRequest
  :super ros::object
  :slots (_weightsfile _maxtime ))

(defmethod arlo_nn_controller::EvaluateDriverRequest
  (:init
   (&key
    ((:weightsfile __weightsfile) "")
    ((:maxtime __maxtime) 0)
    )
   (send-super :init)
   (setq _weightsfile (string __weightsfile))
   (setq _maxtime (round __maxtime))
   self)
  (:weightsfile
   (&optional __weightsfile)
   (if __weightsfile (setq _weightsfile __weightsfile)) _weightsfile)
  (:maxtime
   (&optional __maxtime)
   (if __maxtime (setq _maxtime __maxtime)) _maxtime)
  (:serialization-length
   ()
   (+
    ;; string _weightsfile
    4 (length _weightsfile)
    ;; int64 _maxtime
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _weightsfile
       (write-long (length _weightsfile) s) (princ _weightsfile s)
     ;; int64 _maxtime
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _maxtime (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _maxtime) (= (length (_maxtime . bv)) 2)) ;; bignum
              (write-long (ash (elt (_maxtime . bv) 0) 0) s)
              (write-long (ash (elt (_maxtime . bv) 1) -1) s))
             ((and (class _maxtime) (= (length (_maxtime . bv)) 1)) ;; big1
              (write-long (elt (_maxtime . bv) 0) s)
              (write-long (if (>= _maxtime 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _maxtime s)(write-long (if (>= _maxtime 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _weightsfile
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _weightsfile (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int64 _maxtime
#+(or :alpha :irix6 :x86_64)
      (setf _maxtime (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _maxtime (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(defclass arlo_nn_controller::EvaluateDriverResponse
  :super ros::object
  :slots (_time _dist2go _damage _energy ))

(defmethod arlo_nn_controller::EvaluateDriverResponse
  (:init
   (&key
    ((:time __time) 0.0)
    ((:dist2go __dist2go) 0.0)
    ((:damage __damage) 0.0)
    ((:energy __energy) 0.0)
    )
   (send-super :init)
   (setq _time (float __time))
   (setq _dist2go (float __dist2go))
   (setq _damage (float __damage))
   (setq _energy (float __energy))
   self)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:dist2go
   (&optional __dist2go)
   (if __dist2go (setq _dist2go __dist2go)) _dist2go)
  (:damage
   (&optional __damage)
   (if __damage (setq _damage __damage)) _damage)
  (:energy
   (&optional __energy)
   (if __energy (setq _energy __energy)) _energy)
  (:serialization-length
   ()
   (+
    ;; float64 _time
    8
    ;; float64 _dist2go
    8
    ;; float64 _damage
    8
    ;; float64 _energy
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _time
       (sys::poke _time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dist2go
       (sys::poke _dist2go (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _damage
       (sys::poke _damage (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _energy
       (sys::poke _energy (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _time
     (setq _time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dist2go
     (setq _dist2go (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _damage
     (setq _damage (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _energy
     (setq _energy (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass arlo_nn_controller::EvaluateDriver
  :super ros::object
  :slots ())

(setf (get arlo_nn_controller::EvaluateDriver :md5sum-) "a099938bc78c367ac254aecaded19c78")
(setf (get arlo_nn_controller::EvaluateDriver :datatype-) "arlo_nn_controller/EvaluateDriver")
(setf (get arlo_nn_controller::EvaluateDriver :request) arlo_nn_controller::EvaluateDriverRequest)
(setf (get arlo_nn_controller::EvaluateDriver :response) arlo_nn_controller::EvaluateDriverResponse)

(defmethod arlo_nn_controller::EvaluateDriverRequest
  (:response () (instance arlo_nn_controller::EvaluateDriverResponse :init)))

(setf (get arlo_nn_controller::EvaluateDriverRequest :md5sum-) "a099938bc78c367ac254aecaded19c78")
(setf (get arlo_nn_controller::EvaluateDriverRequest :datatype-) "arlo_nn_controller/EvaluateDriverRequest")
(setf (get arlo_nn_controller::EvaluateDriverRequest :definition-)
      "string weightsfile
int64 maxtime
---
float64 time
float64 dist2go
float64 damage
float64 energy

")

(setf (get arlo_nn_controller::EvaluateDriverResponse :md5sum-) "a099938bc78c367ac254aecaded19c78")
(setf (get arlo_nn_controller::EvaluateDriverResponse :datatype-) "arlo_nn_controller/EvaluateDriverResponse")
(setf (get arlo_nn_controller::EvaluateDriverResponse :definition-)
      "string weightsfile
int64 maxtime
---
float64 time
float64 dist2go
float64 damage
float64 energy

")



(provide :arlo_nn_controller/EvaluateDriver "a099938bc78c367ac254aecaded19c78")


