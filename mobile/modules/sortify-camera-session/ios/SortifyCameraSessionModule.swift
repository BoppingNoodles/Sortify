import AVFoundation
import ExpoCamera
import ExpoModulesCore

public class SortifyCameraSessionModule: Module {
  public func definition() -> ModuleDefinition {
    Name("SortifyCameraSession")

    AsyncFunction("stop") { (viewTag: Int, promise: Promise) in
      guard let view = self.appContext?.findView(withTag: viewTag, ofType: CameraView.self),
            let session = view.session else {
        promise.resolve(false)
        return
      }

      view.sessionQueue.async {
        if session.isRunning {
          session.stopRunning()
        }
        promise.resolve(!session.isRunning)
      }
    }.runOnQueue(.main)
  }
}
