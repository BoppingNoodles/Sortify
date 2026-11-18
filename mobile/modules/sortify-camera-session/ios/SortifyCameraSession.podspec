Pod::Spec.new do |s|
  s.name = 'SortifyCameraSession'
  s.version = '1.0.0'
  s.summary = 'Await iOS camera shutdown before Sortify shutter feedback'
  s.homepage = 'https://github.com/BoppingNoodles/Sortify'
  s.author = 'Sortify'
  s.source = { :git => 'https://github.com/BoppingNoodles/Sortify.git' }
  s.platforms = { :ios => '16.4' }
  s.static_framework = true
  s.source_files = '*.swift'
  s.dependency 'ExpoCamera'
  s.dependency 'ExpoModulesCore'
end
