class validate_params (
  $my_array  = [],
  $my_string = '',
) {
  if "${puppetversion}" =~ /^3\.[6789].*/ {
    fail("Puppet version ${puppetversion} not yet implemented.")
  } # if puppetversion >= 3.6
  elsif "${puppetversion}" =~ /^3\.[012345].*/ {
    validate_array($my_array)
    if size($my_array) == 0 {
      fail("${title}::\$my_array not set")
    }
    validate_string($my_string)
    if size($my_string) == 0 {
      fail("${title}::\$my_string not set")
    }
  }
  else {
    notify {"other version, ${puppetversion}":}
  } # other puppet versions
} # end validate_params

include validate_params
